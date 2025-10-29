"""
Google Drive Manager for GENOMOS Backups

Handles OAuth2 authentication and file operations with Google Drive.
Replaces IPFS for distributed backup storage using Google Workspace.

Philosophy: "Cloud-native distributed backup with organizational ownership"
"""

import os
import pickle
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError
import io

logger = logging.getLogger(__name__)

# Google Drive API scopes
SCOPES = ['https://www.googleapis.com/auth/drive.file']


class GoogleDriveManager:
    """
    Manager for Google Drive operations (OAuth2-based).

    Features:
    - OAuth2 user authentication (opens browser first time)
    - Upload backups to Drive folder
    - Download backups from Drive
    - List all backups
    - Verify backup integrity
    """

    def __init__(
        self,
        client_secret_file: str,
        token_file: str,
        folder_id: str
    ):
        """
        Initialize Google Drive Manager.

        Args:
            client_secret_file: Path to client_secret.json
            token_file: Path to store OAuth2 token (auto-created)
            folder_id: Google Drive folder ID for backups
        """
        self.client_secret_file = client_secret_file
        self.token_file = token_file
        self.folder_id = folder_id
        self.credentials: Optional[Credentials] = None
        self.service = None

        # Authenticate on initialization
        self._authenticate()

    def _authenticate(self):
        """
        Authenticate with Google Drive using OAuth2.

        First time: Opens browser for user authorization
        Subsequent: Uses stored token
        """
        creds = None

        # Load existing token if available
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, 'rb') as token:
                    creds = pickle.load(token)
                logger.info("✅ Loaded existing Google Drive token")
            except Exception as e:
                logger.warning(f"Failed to load token: {e}")

        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    logger.info("✅ Refreshed Google Drive token")
                except Exception as e:
                    logger.error(f"Failed to refresh token: {e}")
                    creds = None

            if not creds:
                # First time: Open browser for authorization
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.client_secret_file, SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                    logger.info("✅ Successfully authenticated with Google Drive")
                except Exception as e:
                    logger.error(f"❌ Failed to authenticate: {e}")
                    raise

            # Save token for future use
            try:
                Path(self.token_file).parent.mkdir(parents=True, exist_ok=True)
                with open(self.token_file, 'wb') as token:
                    pickle.dump(creds, token)
                logger.info(f"✅ Saved token to {self.token_file}")
            except Exception as e:
                logger.warning(f"Failed to save token: {e}")

        self.credentials = creds

        # Build Drive service
        try:
            self.service = build('drive', 'v3', credentials=self.credentials)
            logger.info("✅ Google Drive service initialized")
        except Exception as e:
            logger.error(f"❌ Failed to build Drive service: {e}")
            raise

    def verify_connection(self) -> Dict[str, Any]:
        """
        Verify connection to Google Drive.

        Returns:
            Status dict with connection info
        """
        try:
            # Try to get folder metadata
            folder = self.service.files().get(fileId=self.folder_id).execute()

            return {
                "connected": True,
                "folder_name": folder.get("name"),
                "folder_id": self.folder_id,
                "message": "Google Drive connection verified"
            }
        except HttpError as e:
            logger.error(f"❌ Drive connection failed: {e}")
            return {
                "connected": False,
                "error": str(e),
                "message": "Failed to connect to Google Drive"
            }

    def upload_backup(
        self,
        file_path: str,
        filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload backup file to Google Drive.

        Args:
            file_path: Local path to backup file
            filename: Optional custom filename (default: use original)

        Returns:
            Dict with file_id, name, size, web_view_link
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Backup file not found: {file_path}")

            # Use original filename if not specified
            if not filename:
                filename = Path(file_path).name

            # File metadata
            file_metadata = {
                'name': filename,
                'parents': [self.folder_id],  # Upload to backup folder
                'description': f'GENOMOS backup created {datetime.now().isoformat()}'
            }

            # Media upload
            media = MediaFileUpload(
                file_path,
                mimetype='application/json',
                resumable=True
            )

            # Upload file
            logger.info(f"📤 Uploading {filename} to Google Drive...")
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, size, webViewLink, createdTime'
            ).execute()

            logger.info(f"✅ Upload complete: {file.get('name')} (ID: {file.get('id')})")

            return {
                "success": True,
                "file_id": file.get('id'),
                "name": file.get('name'),
                "size_bytes": int(file.get('size', 0)),
                "web_view_link": file.get('webViewLink'),
                "created_time": file.get('createdTime'),
                "message": f"Backup uploaded successfully"
            }

        except Exception as e:
            logger.error(f"❌ Upload failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to upload backup"
            }

    def download_backup(
        self,
        file_id: str,
        output_path: str
    ) -> Dict[str, Any]:
        """
        Download backup from Google Drive.

        Args:
            file_id: Google Drive file ID
            output_path: Local path to save file

        Returns:
            Status dict
        """
        try:
            # Get file metadata
            file_metadata = self.service.files().get(fileId=file_id).execute()

            logger.info(f"📥 Downloading {file_metadata.get('name')} from Google Drive...")

            # Download file
            request = self.service.files().get_media(fileId=file_id)

            # Create output directory if needed
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

            # Download to file
            fh = io.FileIO(output_path, 'wb')
            downloader = MediaIoBaseDownload(fh, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    logger.info(f"Download progress: {int(status.progress() * 100)}%")

            fh.close()

            logger.info(f"✅ Download complete: {output_path}")

            return {
                "success": True,
                "file_id": file_id,
                "name": file_metadata.get('name'),
                "output_path": output_path,
                "size_bytes": int(file_metadata.get('size', 0)),
                "message": "Backup downloaded successfully"
            }

        except HttpError as e:
            logger.error(f"❌ Download failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to download backup"
            }

    def list_backups(self, limit: int = 50) -> Dict[str, Any]:
        """
        List all backups in Drive folder.

        Args:
            limit: Max number of files to return

        Returns:
            Dict with list of backup files
        """
        try:
            # Query for files in backup folder
            query = f"'{self.folder_id}' in parents and trashed=false"

            results = self.service.files().list(
                q=query,
                pageSize=limit,
                fields="files(id, name, size, createdTime, modifiedTime, webViewLink)",
                orderBy="createdTime desc"
            ).execute()

            files = results.get('files', [])

            logger.info(f"✅ Found {len(files)} backups in Drive")

            return {
                "success": True,
                "count": len(files),
                "backups": [
                    {
                        "file_id": f.get('id'),
                        "name": f.get('name'),
                        "size_bytes": int(f.get('size', 0)),
                        "created_time": f.get('createdTime'),
                        "modified_time": f.get('modifiedTime'),
                        "web_view_link": f.get('webViewLink')
                    }
                    for f in files
                ]
            }

        except HttpError as e:
            logger.error(f"❌ Failed to list backups: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to list backups"
            }

    def delete_backup(self, file_id: str) -> Dict[str, Any]:
        """
        Delete backup from Google Drive.

        Args:
            file_id: Google Drive file ID

        Returns:
            Status dict
        """
        try:
            # Get file name before deleting
            file_metadata = self.service.files().get(fileId=file_id).execute()
            filename = file_metadata.get('name')

            # Delete file
            self.service.files().delete(fileId=file_id).execute()

            logger.info(f"✅ Deleted backup: {filename}")

            return {
                "success": True,
                "file_id": file_id,
                "name": filename,
                "message": "Backup deleted successfully"
            }

        except HttpError as e:
            logger.error(f"❌ Failed to delete backup: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to delete backup"
            }


# Initialize global instance (will be initialized by main.py)
_drive_manager: Optional[GoogleDriveManager] = None


def initialize_drive_manager(
    client_secret_file: str,
    token_file: str,
    folder_id: str
) -> GoogleDriveManager:
    """Initialize global GoogleDriveManager instance."""
    global _drive_manager
    _drive_manager = GoogleDriveManager(client_secret_file, token_file, folder_id)
    return _drive_manager


def get_drive_manager() -> Optional[GoogleDriveManager]:
    """Get global GoogleDriveManager instance."""
    return _drive_manager