#!/usr/bin/env python3
"""
Sync Knowledge Base to CSN Shared Drive

Bidirectional sync between Git repo (knowledge_base_structured/) and
CSN Shared Drive (cognitivesovereignty.network Google Workspace).

Features:
- Upload new files from Git to Drive
- Download new files from Drive to Git
- Detect conflicts (both sides modified)
- Dry-run mode for safe testing
- Multiple sync modes: voktere, dimensjoner, pulser, all

Usage:
    python scripts/sync_to_csn_drive.py --mode all --dry-run
    python scripts/sync_to_csn_drive.py --mode voktere --direction to-drive
    python scripts/sync_to_csn_drive.py --mode all --conflict-strategy newest

Author: Code (Agent #9)
Date: 29. oktober 2025
"""

import os
import sys
import json
import hashlib
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging

# Add ubuntu-playground to path
sys.path.insert(0, str(Path(__file__).parent.parent / "ubuntu-playground"))

from api.blockchain.google_drive_manager import GoogleDriveManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CSNKnowledgeSync:
    """Sync knowledge base between Git and CSN Drive."""

    def __init__(
        self,
        repo_root: Path,
        drive_manager: GoogleDriveManager,
        folder_mapping: Dict[str, str],
        dry_run: bool = False
    ):
        """
        Initialize sync manager.

        Args:
            repo_root: Repository root path
            drive_manager: GoogleDriveManager instance
            folder_mapping: Dict mapping category to Drive folder ID
            dry_run: If True, only show what would be done
        """
        self.repo_root = repo_root
        self.drive_manager = drive_manager
        self.folder_mapping = folder_mapping
        self.dry_run = dry_run

        self.local_base = repo_root / "knowledge_base_structured"

        # Stats
        self.stats = {
            "local_files": 0,
            "drive_files": 0,
            "uploaded": 0,
            "downloaded": 0,
            "updated": 0,
            "conflicts": 0,
            "skipped": 0
        }

    def calculate_md5(self, file_path: Path) -> str:
        """Calculate MD5 hash of local file."""
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5.update(chunk)
        return md5.hexdigest()

    def scan_local_folder(self, category: str) -> Dict[str, Dict]:
        """
        Scan local folder for files.

        Args:
            category: Category name (voktere, dimensjoner, pulser)

        Returns:
            Dict mapping relative_path → file info
        """
        local_folder = self.local_base / category
        if not local_folder.exists():
            logger.warning(f"⚠️ Local folder not found: {local_folder}")
            return {}

        files = {}

        # Recursively find all .md files
        for md_file in local_folder.rglob("*.md"):
            relative_path = md_file.relative_to(local_folder)
            relative_path_str = str(relative_path).replace("\\", "/")

            files[relative_path_str] = {
                "local_path": str(md_file),
                "modified_time": datetime.fromtimestamp(md_file.stat().st_mtime).isoformat(),
                "md5": self.calculate_md5(md_file),
                "size": md_file.stat().st_size
            }

        self.stats["local_files"] += len(files)
        return files

    def scan_drive_folder(self, category: str) -> Dict[str, Dict]:
        """
        Scan Drive folder for files.

        Args:
            category: Category name (voktere, dimensjoner, pulser)

        Returns:
            Dict mapping relative_path → file info
        """
        drive_folder_id = self.folder_mapping.get(category)
        if not drive_folder_id:
            logger.warning(f"⚠️ No Drive folder ID for category: {category}")
            return {}

        logger.info(f"Scanning Drive folder: {category} (ID: {drive_folder_id})")

        # List all files recursively
        drive_files_list = self.drive_manager.list_files_recursive(
            folder_id=drive_folder_id,
            mime_type='text/markdown'
        )

        files = {}
        for file_info in drive_files_list:
            relative_path = file_info['path']

            files[relative_path] = {
                "drive_id": file_info['id'],
                "modified_time": file_info['modified_time'],
                "md5": file_info['md5'],
                "size": file_info['size']
            }

        self.stats["drive_files"] += len(files)
        return files

    def compare_files(
        self,
        local_files: Dict[str, Dict],
        drive_files: Dict[str, Dict]
    ) -> Tuple[List[str], List[str], List[str], List[str]]:
        """
        Compare local and Drive files.

        Args:
            local_files: Local file dict
            drive_files: Drive file dict

        Returns:
            Tuple of (new_local, new_drive, updated_local, conflicts)
        """
        new_local = []    # Files only in local (need upload)
        new_drive = []    # Files only in Drive (need download)
        updated_local = []  # Files in both, local is newer
        conflicts = []    # Files modified in both places

        # Check local files
        for path, local_info in local_files.items():
            if path not in drive_files:
                new_local.append(path)
            else:
                drive_info = drive_files[path]

                # Compare MD5
                if local_info['md5'] != drive_info['md5']:
                    # Files differ - check timestamps
                    local_time = datetime.fromisoformat(local_info['modified_time'].replace('Z', '+00:00'))
                    drive_time = datetime.fromisoformat(drive_info['modified_time'].replace('Z', '+00:00'))

                    # Allow 2 second tolerance for timestamp comparison
                    time_diff = abs((local_time - drive_time).total_seconds())

                    if time_diff > 2:
                        if local_time > drive_time:
                            updated_local.append(path)
                        else:
                            # Drive is newer - potential conflict
                            conflicts.append(path)

        # Check Drive files
        for path in drive_files:
            if path not in local_files:
                new_drive.append(path)

        return new_local, new_drive, updated_local, conflicts

    def sync_category(
        self,
        category: str,
        direction: str = "bidirectional",
        conflict_strategy: str = "ask"
    ):
        """
        Sync single category.

        Args:
            category: Category name (voktere, dimensjoner, pulser)
            direction: "to-drive", "from-drive", "bidirectional"
            conflict_strategy: "ask", "local_wins", "drive_wins", "newest"
        """
        logger.info("=" * 70)
        logger.info(f"SYNCING: {category.upper()}")
        logger.info("=" * 70)

        # Scan local and Drive folders
        local_files = self.scan_local_folder(category)
        drive_files = self.scan_drive_folder(category)

        logger.info(f"Local files: {len(local_files)}")
        logger.info(f"Drive files: {len(drive_files)}")

        # Compare files
        new_local, new_drive, updated_local, conflicts = self.compare_files(
            local_files, drive_files
        )

        logger.info(f"New local files: {len(new_local)}")
        logger.info(f"New Drive files: {len(new_drive)}")
        logger.info(f"Updated local files: {len(updated_local)}")
        logger.info(f"Conflicts: {len(conflicts)}")
        logger.info("")

        # Upload new local files to Drive
        if direction in ["to-drive", "bidirectional"] and new_local:
            logger.info("📤 Uploading new local files to Drive...")
            for path in new_local:
                self._upload_file(category, path, local_files[path])

        # Upload updated local files to Drive
        if direction in ["to-drive", "bidirectional"] and updated_local:
            logger.info("📤 Updating Drive files with newer local versions...")
            for path in updated_local:
                self._update_file(category, path, local_files[path], drive_files[path])

        # Download new Drive files to local
        if direction in ["from-drive", "bidirectional"] and new_drive:
            logger.info("📥 Downloading new Drive files to local...")
            for path in new_drive:
                self._download_file(category, path, drive_files[path])

        # Handle conflicts
        if conflicts:
            logger.info("⚠️ Handling conflicts...")
            for path in conflicts:
                self._handle_conflict(
                    category, path,
                    local_files[path], drive_files[path],
                    conflict_strategy
                )

        logger.info("")
        self.stats["conflicts"] += len(conflicts)

    def _upload_file(self, category: str, path: str, local_info: Dict):
        """Upload new file to Drive."""
        if self.dry_run:
            logger.info(f"  [DRY-RUN] Would upload: {path}")
            return

        drive_folder_id = self.folder_mapping.get(category)
        local_path = local_info['local_path']

        # Determine target folder (handle subfolders)
        if "/" in path:
            # File is in subfolder (e.g., "01_filosofi_etikk/01_Kant.md")
            subfolder = path.split("/")[0]
            filename = path.split("/")[-1]

            # Find or create subfolder in Drive
            # For simplicity, we'll use the category root for now
            # TODO: Implement subfolder support
            target_folder_id = drive_folder_id
        else:
            filename = path
            target_folder_id = drive_folder_id

        result = self.drive_manager.upload_file(
            local_path=local_path,
            drive_folder_id=target_folder_id,
            filename=filename
        )

        if result.get('success'):
            logger.info(f"  ✅ Uploaded: {path}")
            self.stats["uploaded"] += 1
        else:
            logger.error(f"  ❌ Failed to upload: {path} - {result.get('error')}")

    def _update_file(self, category: str, path: str, local_info: Dict, drive_info: Dict):
        """Update existing Drive file with local version."""
        if self.dry_run:
            logger.info(f"  [DRY-RUN] Would update: {path}")
            return

        local_path = local_info['local_path']
        drive_file_id = drive_info['drive_id']

        result = self.drive_manager.update_file(
            file_id=drive_file_id,
            local_path=local_path
        )

        if result.get('success'):
            logger.info(f"  ✅ Updated: {path}")
            self.stats["updated"] += 1
        else:
            logger.error(f"  ❌ Failed to update: {path} - {result.get('error')}")

    def _download_file(self, category: str, path: str, drive_info: Dict):
        """Download Drive file to local."""
        if self.dry_run:
            logger.info(f"  [DRY-RUN] Would download: {path}")
            return

        drive_file_id = drive_info['drive_id']
        local_path = self.local_base / category / path

        # Create parent directory if needed
        local_path.parent.mkdir(parents=True, exist_ok=True)

        result = self.drive_manager.download_backup(
            file_id=drive_file_id,
            output_path=str(local_path)
        )

        if result.get('success'):
            logger.info(f"  ✅ Downloaded: {path}")
            self.stats["downloaded"] += 1
        else:
            logger.error(f"  ❌ Failed to download: {path} - {result.get('error')}")

    def _handle_conflict(
        self,
        category: str,
        path: str,
        local_info: Dict,
        drive_info: Dict,
        strategy: str
    ):
        """Handle file conflict."""
        if self.dry_run:
            logger.info(f"  [DRY-RUN] Conflict detected: {path}")
            return

        logger.warning(f"  ⚠️ CONFLICT: {path}")
        logger.warning(f"     Local modified: {local_info['modified_time']}")
        logger.warning(f"     Drive modified: {drive_info['modified_time']}")

        if strategy == "local_wins":
            logger.info(f"     → Strategy: local_wins - Uploading local version")
            self._update_file(category, path, local_info, drive_info)
        elif strategy == "drive_wins":
            logger.info(f"     → Strategy: drive_wins - Downloading Drive version")
            self._download_file(category, path, drive_info)
        elif strategy == "newest":
            local_time = datetime.fromisoformat(local_info['modified_time'].replace('Z', '+00:00'))
            drive_time = datetime.fromisoformat(drive_info['modified_time'].replace('Z', '+00:00'))

            if local_time > drive_time:
                logger.info(f"     → Strategy: newest - Local is newer, uploading")
                self._update_file(category, path, local_info, drive_info)
            else:
                logger.info(f"     → Strategy: newest - Drive is newer, downloading")
                self._download_file(category, path, drive_info)
        else:  # ask
            logger.warning(f"     → Strategy: ask - Manual resolution required")
            self.stats["skipped"] += 1

    def sync_all(
        self,
        direction: str = "bidirectional",
        conflict_strategy: str = "ask"
    ):
        """Sync all categories."""
        categories = ["voktere", "dimensjoner", "pulser"]

        for category in categories:
            if category in self.folder_mapping:
                self.sync_category(category, direction, conflict_strategy)
            else:
                logger.warning(f"⚠️ Skipping {category} - no folder mapping")

    def print_summary(self):
        """Print sync summary."""
        logger.info("=" * 70)
        logger.info("SYNC SUMMARY")
        logger.info("=" * 70)
        logger.info(f"Local files scanned: {self.stats['local_files']}")
        logger.info(f"Drive files scanned: {self.stats['drive_files']}")
        logger.info(f"Files uploaded: {self.stats['uploaded']}")
        logger.info(f"Files downloaded: {self.stats['downloaded']}")
        logger.info(f"Files updated: {self.stats['updated']}")
        logger.info(f"Conflicts detected: {self.stats['conflicts']}")
        logger.info(f"Files skipped: {self.stats['skipped']}")
        logger.info("=" * 70)


def load_folder_mapping(mapping_file: Path) -> Dict[str, str]:
    """Load CSN folder mapping from JSON file."""
    if not mapping_file.exists():
        logger.error(f"❌ Folder mapping file not found: {mapping_file}")
        logger.info("Run: python scripts/setup_csn_knowledge_base.py")
        sys.exit(1)

    with open(mapping_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Map categories to their Drive folder IDs (from CSN_FOLDER_IDS.json)
    mapping = {
        "voktere": data.get("01_Knowledge_Base/voktere"),
        "dimensjoner": data.get("01_Knowledge_Base/dimensjoner"),
        "pulser": data.get("01_Knowledge_Base/pulser")
    }

    # Remove None values
    mapping = {k: v for k, v in mapping.items() if v}

    if not mapping:
        logger.error("❌ No valid folder mappings found in CSN_FOLDER_IDS.json")
        sys.exit(1)

    return mapping


def main():
    """Main execution."""
    parser = argparse.ArgumentParser(
        description="Sync knowledge base between Git and CSN Drive"
    )
    parser.add_argument(
        "--mode",
        choices=["voktere", "dimensjoner", "pulser", "all"],
        default="all",
        help="Sync mode (default: all)"
    )
    parser.add_argument(
        "--direction",
        choices=["to-drive", "from-drive", "bidirectional"],
        default="bidirectional",
        help="Sync direction (default: bidirectional)"
    )
    parser.add_argument(
        "--conflict-strategy",
        choices=["ask", "local_wins", "drive_wins", "newest"],
        default="newest",
        help="Conflict resolution strategy (default: newest)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry run mode - show what would be done without doing it"
    )

    args = parser.parse_args()

    # Paths
    repo_root = Path(__file__).parent.parent
    mapping_file = repo_root / "CSN_FOLDER_IDS.json"

    # Load environment
    from dotenv import load_dotenv
    load_dotenv(repo_root / ".env")

    client_secret_file = repo_root / os.getenv("GOOGLE_CLIENT_SECRET_FILE")
    token_file = repo_root / os.getenv("GOOGLE_TOKEN_FILE")
    csn_root = os.getenv("CSN_SHARED_DRIVE_ROOT")

    logger.info("=" * 70)
    logger.info("CSN KNOWLEDGE BASE SYNC")
    logger.info("=" * 70)
    logger.info(f"Mode: {args.mode}")
    logger.info(f"Direction: {args.direction}")
    logger.info(f"Conflict strategy: {args.conflict_strategy}")
    logger.info(f"Dry run: {args.dry_run}")
    logger.info("")

    # Load folder mapping
    logger.info(f"Loading folder mapping from: {mapping_file}")
    folder_mapping = load_folder_mapping(mapping_file)
    logger.info(f"Found {len(folder_mapping)} category mappings")
    logger.info("")

    # Initialize Drive manager
    logger.info("Initializing Google Drive connection...")
    drive_manager = GoogleDriveManager(
        client_secret_file=str(client_secret_file),
        token_file=str(token_file),
        folder_id=csn_root
    )

    # Note: Skip verify_connection() for shared drive root (it's a special ID)
    logger.info(f"✅ Connected to CSN Shared Drive (ID: {csn_root})")
    logger.info("")

    # Create sync manager
    sync = CSNKnowledgeSync(
        repo_root=repo_root,
        drive_manager=drive_manager,
        folder_mapping=folder_mapping,
        dry_run=args.dry_run
    )

    # Sync
    if args.mode == "all":
        sync.sync_all(args.direction, args.conflict_strategy)
    else:
        sync.sync_category(args.mode, args.direction, args.conflict_strategy)

    # Print summary
    sync.print_summary()

    logger.info("")
    logger.info("Next steps:")
    logger.info("  1. Verify files in CSN Drive: https://drive.google.com/drive/folders/0AHnSqf7b5sRDUk9PVA")
    logger.info("  2. Test conflict detection by editing same file in both places")
    logger.info("  3. Set up automated sync (cron job or GitHub Actions)")
    logger.info("")


if __name__ == "__main__":
    main()
