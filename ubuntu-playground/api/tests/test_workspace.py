"""
Workspace Integration Tests

Tests for file operations, agent permissions, and workspace management.
"""
import pytest
from pathlib import Path
from fastapi.testclient import TestClient


@pytest.mark.unit
@pytest.mark.workspace
class TestWorkspaceFileOperations:
    """Test basic file operations in workspace"""

    def test_create_file(self, client: TestClient, aurora_api_key: str, sample_file_content: str):
        """Test creating a file in Aurora workspace"""
        response = client.post(
            "/workspace/aurora/research-notes.md",
            json={"content": sample_file_content},
            headers={"X-Agent-API-Key": aurora_api_key}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "created"
        assert data["path"] == "aurora/research-notes.md"
        assert "size" in data

    def test_read_file(self, client: TestClient, aurora_api_key: str, sample_file_content: str):
        """Test reading a file from workspace"""
        # First create file
        client.post(
            "/workspace/aurora/test-read.md",
            json={"content": sample_file_content},
            headers={"X-Agent-API-Key": aurora_api_key}
        )

        # Then read it
        response = client.get(
            "/workspace/aurora/test-read.md",
            headers={"X-Agent-API-Key": aurora_api_key}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["content"] == sample_file_content
        assert data["path"] == "aurora/test-read.md"

    def test_update_file(self, client: TestClient, aurora_api_key: str):
        """Test updating existing file"""
        # Create file
        original_content = "Original content"
        client.post(
            "/workspace/aurora/update-test.md",
            json={"content": original_content},
            headers={"X-Agent-API-Key": aurora_api_key}
        )

        # Update file
        updated_content = "Updated content"
        response = client.put(
            "/workspace/aurora/update-test.md",
            json={"content": updated_content},
            headers={"X-Agent-API-Key": aurora_api_key}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "updated"

        # Verify update
        read_response = client.get(
            "/workspace/aurora/update-test.md",
            headers={"X-Agent-API-Key": aurora_api_key}
        )
        assert read_response.json()["content"] == updated_content

    def test_delete_file(self, client: TestClient, aurora_api_key: str):
        """Test deleting a file"""
        # Create file
        client.post(
            "/workspace/aurora/delete-test.md",
            json={"content": "To be deleted"},
            headers={"X-Agent-API-Key": aurora_api_key}
        )

        # Delete file
        response = client.delete(
            "/workspace/aurora/delete-test.md",
            headers={"X-Agent-API-Key": aurora_api_key}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "deleted"

        # Verify deletion
        read_response = client.get(
            "/workspace/aurora/delete-test.md",
            headers={"X-Agent-API-Key": aurora_api_key}
        )
        assert read_response.status_code == 404

    def test_list_files(self, client: TestClient, aurora_api_key: str):
        """Test listing files in workspace"""
        # Create multiple files
        for i in range(3):
            client.post(
                f"/workspace/aurora/file-{i}.md",
                json={"content": f"Content {i}"},
                headers={"X-Agent-API-Key": aurora_api_key}
            )

        # List files
        response = client.get(
            "/workspace/aurora",
            headers={"X-Agent-API-Key": aurora_api_key}
        )

        assert response.status_code == 200
        data = response.json()
        assert "files" in data
        assert len(data["files"]) >= 3


@pytest.mark.unit
@pytest.mark.workspace
class TestAgentPermissions:
    """Test agent-specific permissions"""

    def test_agent_can_write_own_workspace(self, client: TestClient, aurora_api_key: str):
        """Test agent can write to own workspace"""
        response = client.post(
            "/workspace/aurora/own-file.md",
            json={"content": "Aurora's own file"},
            headers={"X-Agent-API-Key": aurora_api_key}
        )

        assert response.status_code == 201

    def test_agent_can_write_shared_workspace(self, client: TestClient, aurora_api_key: str):
        """Test agent can write to shared workspace"""
        response = client.post(
            "/workspace/shared/collective-notes.md",
            json={"content": "Shared research notes"},
            headers={"X-Agent-API-Key": aurora_api_key}
        )

        assert response.status_code == 201

    def test_agent_cannot_write_other_workspace(self, client: TestClient, aurora_api_key: str):
        """Test agent cannot write to another agent's workspace"""
        response = client.post(
            "/workspace/lira/restricted-file.md",
            json={"content": "Trying to access Lira's workspace"},
            headers={"X-Agent-API-Key": aurora_api_key}
        )

        # Should fail with 403 Forbidden
        assert response.status_code == 403

    def test_agent_can_read_all(self, client: TestClient, aurora_api_key: str, lira_api_key: str):
        """Test agent can read from all workspaces (read:all permission)"""
        # Lira creates file in her workspace
        client.post(
            "/workspace/lira/biofield-data.md",
            json={"content": "Lira's biofield analysis"},
            headers={"X-Agent-API-Key": lira_api_key}
        )

        # Aurora reads Lira's file (has read:all permission)
        response = client.get(
            "/workspace/lira/biofield-data.md",
            headers={"X-Agent-API-Key": aurora_api_key}
        )

        assert response.status_code == 200

    def test_invalid_api_key(self, client: TestClient):
        """Test request with invalid API key"""
        response = client.post(
            "/workspace/aurora/test.md",
            json={"content": "Test"},
            headers={"X-Agent-API-Key": "invalid-key"}
        )

        assert response.status_code == 401


@pytest.mark.unit
@pytest.mark.workspace
class TestWorkspaceEvents:
    """Test workspace event logging"""

    def test_file_create_logged(self, client: TestClient, aurora_api_key: str):
        """Test file creation is logged to SQLite"""
        response = client.post(
            "/workspace/aurora/logged-file.md",
            json={"content": "This should be logged"},
            headers={"X-Agent-API-Key": aurora_api_key}
        )

        assert response.status_code == 201

        # Check events log
        events_response = client.get(
            "/events",
            headers={"X-Agent-API-Key": aurora_api_key}
        )

        assert events_response.status_code == 200
        events = events_response.json()

        # Verify event exists
        create_events = [e for e in events if e["action"] == "create" and "aurora/logged-file.md" in e["path"]]
        assert len(create_events) > 0

    def test_events_have_timestamp(self, client: TestClient, aurora_api_key: str):
        """Test all events have valid timestamps"""
        client.post(
            "/workspace/aurora/timestamp-test.md",
            json={"content": "Test"},
            headers={"X-Agent-API-Key": aurora_api_key}
        )

        events_response = client.get(
            "/events",
            headers={"X-Agent-API-Key": aurora_api_key}
        )

        events = events_response.json()
        for event in events:
            assert "timestamp" in event
            assert event["timestamp"] is not None
