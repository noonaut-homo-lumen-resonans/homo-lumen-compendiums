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

# Google Drive API scopes (includes Sheets for GENOMOS integration)
# NOTE: 'drive' (not 'drive.file') is required to access existing shared folders
# 'drive.file' only grants access to files/folders created by the app
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets'
]


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
        Verify connection to Google Drive (supports Shared Drives).

        Returns:
            Status dict with connection info
        """
        try:
            # Try to get folder metadata (supports Shared Drives)
            folder = self.service.files().get(
                fileId=self.folder_id,
                supportsAllDrives=True
            ).execute()

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

            # Upload file (supports Shared Drives)
            logger.info(f"📤 Uploading {filename} to Google Drive...")
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, size, webViewLink, createdTime',
                supportsAllDrives=True
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
            # Get file metadata (supports Shared Drives)
            file_metadata = self.service.files().get(
                fileId=file_id,
                supportsAllDrives=True
            ).execute()

            logger.info(f"📥 Downloading {file_metadata.get('name')} from Google Drive...")

            # Download file (supports Shared Drives)
            request = self.service.files().get_media(
                fileId=file_id,
                supportsAllDrives=True
            )

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
            # Query for files in backup folder (supports Shared Drives)
            query = f"'{self.folder_id}' in parents and trashed=false"

            results = self.service.files().list(
                q=query,
                pageSize=limit,
                fields="files(id, name, size, createdTime, modifiedTime, webViewLink)",
                orderBy="createdTime desc",
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
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
            # Get file name before deleting (supports Shared Drives)
            file_metadata = self.service.files().get(
                fileId=file_id,
                supportsAllDrives=True
            ).execute()
            filename = file_metadata.get('name')

            # Delete file (supports Shared Drives)
            self.service.files().delete(
                fileId=file_id,
                supportsAllDrives=True
            ).execute()

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

    # =========================================================================
    # SYNC METHODS (for bidirectional Git ↔ Drive sync)
    # =========================================================================

    def list_files_recursive(
        self,
        folder_id: str,
        mime_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List all files in folder recursively (including subfolders).

        Args:
            folder_id: Google Drive folder ID
            mime_type: Optional mime type filter (e.g., 'text/markdown')

        Returns:
            List of file dicts with id, name, path, modified_time, md5, size
        """
        all_files = []

        def _list_folder(parent_id: str, parent_path: str = ""):
            """Recursively list folder contents."""
            try:
                # Query for items in this folder
                query = f"'{parent_id}' in parents and trashed=false"
                if mime_type:
                    query += f" and mimeType='{mime_type}'"

                page_token = None
                while True:
                    results = self.service.files().list(
                        q=query,
                        pageSize=100,
                        fields="nextPageToken, files(id, name, mimeType, modifiedTime, md5Checksum, size)",
                        pageToken=page_token,
                        supportsAllDrives=True,
                        includeItemsFromAllDrives=True
                    ).execute()

                    items = results.get('files', [])

                    for item in items:
                        item_type = item.get('mimeType')
                        item_name = item.get('name')
                        item_path = f"{parent_path}/{item_name}" if parent_path else item_name

                        if item_type == 'application/vnd.google-apps.folder':
                            # Recursively list subfolder
                            _list_folder(item.get('id'), item_path)
                        else:
                            # Add file to list
                            all_files.append({
                                "id": item.get('id'),
                                "name": item_name,
                                "path": item_path,
                                "modified_time": item.get('modifiedTime'),
                                "md5": item.get('md5Checksum'),
                                "size": int(item.get('size', 0))
                            })

                    page_token = results.get('nextPageToken')
                    if not page_token:
                        break

            except HttpError as e:
                logger.error(f"❌ Failed to list folder {parent_id}: {e}")

        _list_folder(folder_id)
        return all_files

    def upload_file(
        self,
        local_path: str,
        drive_folder_id: str,
        filename: Optional[str] = None,
        mime_type: str = 'text/markdown'
    ) -> Dict[str, Any]:
        """
        Upload file to specific Drive folder.

        Args:
            local_path: Local file path
            drive_folder_id: Drive folder ID
            filename: Optional custom filename
            mime_type: File mime type (default: text/markdown)

        Returns:
            Dict with file_id, name, modified_time, md5
        """
        try:
            if not os.path.exists(local_path):
                raise FileNotFoundError(f"File not found: {local_path}")

            if not filename:
                filename = Path(local_path).name

            # File metadata
            file_metadata = {
                'name': filename,
                'parents': [drive_folder_id]
            }

            # Media upload
            media = MediaFileUpload(
                local_path,
                mimetype=mime_type,
                resumable=True
            )

            # Upload file
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, modifiedTime, md5Checksum, size',
                supportsAllDrives=True
            ).execute()

            return {
                "success": True,
                "file_id": file.get('id'),
                "name": file.get('name'),
                "modified_time": file.get('modifiedTime'),
                "md5": file.get('md5Checksum'),
                "size": int(file.get('size', 0))
            }

        except Exception as e:
            logger.error(f"❌ Upload failed for {local_path}: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def update_file(
        self,
        file_id: str,
        local_path: str,
        mime_type: str = 'text/markdown'
    ) -> Dict[str, Any]:
        """
        Update existing Drive file with new content.

        Args:
            file_id: Drive file ID to update
            local_path: Local file path with new content
            mime_type: File mime type

        Returns:
            Dict with file_id, name, modified_time, md5
        """
        try:
            if not os.path.exists(local_path):
                raise FileNotFoundError(f"File not found: {local_path}")

            # Media upload
            media = MediaFileUpload(
                local_path,
                mimetype=mime_type,
                resumable=True
            )

            # Update file
            file = self.service.files().update(
                fileId=file_id,
                media_body=media,
                fields='id, name, modifiedTime, md5Checksum, size',
                supportsAllDrives=True
            ).execute()

            return {
                "success": True,
                "file_id": file.get('id'),
                "name": file.get('name'),
                "modified_time": file.get('modifiedTime'),
                "md5": file.get('md5Checksum'),
                "size": int(file.get('size', 0))
            }

        except Exception as e:
            logger.error(f"❌ Update failed for {file_id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def get_file_metadata(self, file_id: str) -> Dict[str, Any]:
        """
        Get file metadata (timestamps, MD5, size).

        Args:
            file_id: Drive file ID

        Returns:
            Dict with id, name, modified_time, md5, size
        """
        try:
            file = self.service.files().get(
                fileId=file_id,
                fields='id, name, modifiedTime, md5Checksum, size',
                supportsAllDrives=True
            ).execute()

            return {
                "success": True,
                "id": file.get('id'),
                "name": file.get('name'),
                "modified_time": file.get('modifiedTime'),
                "md5": file.get('md5Checksum'),
                "size": int(file.get('size', 0))
            }

        except HttpError as e:
            logger.error(f"❌ Failed to get metadata for {file_id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def create_folder(
        self,
        folder_name: str,
        parent_id: str,
        description: str = ""
    ) -> Optional[str]:
        """
        Create folder in Drive.

        Args:
            folder_name: Name of folder to create
            parent_id: Parent folder ID
            description: Optional folder description

        Returns:
            Folder ID if successful, None otherwise
        """
        try:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_id]
            }
            if description:
                file_metadata['description'] = description

            folder = self.service.files().create(
                body=file_metadata,
                fields='id, name',
                supportsAllDrives=True
            ).execute()

            logger.info(f"✅ Created folder: {folder_name} (ID: {folder.get('id')})")
            return folder.get('id')

        except HttpError as e:
            logger.error(f"❌ Failed to create folder {folder_name}: {e}")
            return None


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