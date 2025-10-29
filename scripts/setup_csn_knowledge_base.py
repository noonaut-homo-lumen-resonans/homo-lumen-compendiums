#!/usr/bin/env python3
"""
Setup CSN Knowledge Base Folder Structure

Creates the following structure in CSN Shared Drive (Genomos):
- 01_Knowledge_Base/
  - voktere/ (5 category subfolders)
  - dimensjoner/ (3 grouping subfolders)
  - pulser/
- 02_Agent_Coalition/ (10 agent subfolders)
- 03_SMK_Strategic_Docs/
- 04_Kompendium_Chapters/
- 05_Collaboration/
  - drafts/
  - reviews/
  - archive/

Usage:
    python scripts/setup_csn_knowledge_base.py

Output:
    - Folders created in CSN Drive
    - CSN_FOLDER_IDS.json (folder ID mapping)
    - .env updated with folder IDs

Author: Code (Agent #9)
Date: 29. oktober 2025
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any
import logging

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "ubuntu-playground" / "api"))

from blockchain.google_drive_manager import GoogleDriveManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Folder structure to create
FOLDER_STRUCTURE = {
    "01_Knowledge_Base": {
        "description": "Voktere, Dimensjoner, Pulser - Source of truth",
        "subfolders": {
            "voktere": {
                "description": "40+ Knowledge Guardians organized by category",
                "subfolders": {
                    "01_filosofi_etikk": {"description": "Kant, Heidegger, Levinas, Kierkegaard, etc."},
                    "02_psykologi": {"description": "Jung, Rogers, Porges, Brené Brown, etc."},
                    "03_fysikk_systemer": {"description": "Bohm, Capra, Faggin, Sheldrake, etc."},
                    "04_teknologi_sikkerhet": {"description": "Schneier, Snowden, Zimmermann, etc."},
                    "05_kritisk_teori": {"description": "Taleb, Latour, McKenna, Thich Nhat Hanh, etc."}
                }
            },
            "dimensjoner": {
                "description": "13 Consciousness Dimensions (D00-D12)",
                "subfolders": {
                    "D00_D04": {"description": "Fundamentale dimensjoner (Quantum → Heart)"},
                    "D05_D08": {"description": "Arketypiske dimensjoner (Pattern → Morphic)"},
                    "D09_D12": {"description": "Transcendente dimensjoner (Atemporal → Source)"}
                }
            },
            "pulser": {
                "description": "Rhythmic practices and embodiment",
                "subfolders": {
                    "praksis": {"description": "Practical implementation guides"}
                }
            }
        }
    },
    "02_Agent_Coalition": {
        "description": "10 Agents - Instructions, logs, living knowledge",
        "subfolders": {
            "orion": {"description": "Hjertets Koordinator - Meta-coordination"},
            "lira": {"description": "Feltets Stemme - Biofelt integration"},
            "nyra": {"description": "Vindu-skaper - Visual architecture"},
            "thalus": {"description": "Ontologisk Vokter - Ethical foundation"},
            "zara": {"description": "Grense-Vokter - Security & boundaries"},
            "abacus": {"description": "Mønster-Lytter - Pattern recognition"},
            "aurora": {"description": "Epistemisk Bro - Research & knowledge"},
            "manus": {"description": "Resonanskammer-Arkitekt - Design & structure"},
            "code": {"description": "Resonanskammer-Implementør - Technical implementation"},
            "falcon": {"description": "Tidsveven-Navigatør - Temporal coordination"}
        }
    },
    "03_SMK_Strategic_Docs": {
        "description": "Strategic Macro-Coordination (SMK#001-050+)",
        "subfolders": {}
    },
    "04_Kompendium_Chapters": {
        "description": "Homo Lumen Kompendium V20.11 (KAPITTEL_01-12)",
        "subfolders": {}
    },
    "05_Collaboration": {
        "description": "Stakeholder edits and collaboration space",
        "subfolders": {
            "drafts": {"description": "Work-in-progress edits from stakeholders"},
            "reviews": {"description": "Pending merge to knowledge base"},
            "archive": {"description": "Merged content (historical record)"}
        }
    }
}

# 10 Agent names for folder creation
AGENTS = [
    "orion", "lira", "nyra", "thalus", "zara",
    "abacus", "aurora", "manus", "code", "falcon"
]


class CSNKnowledgeBaseSetup:
    """Setup CSN Knowledge Base folder structure in Google Drive."""

    def __init__(self, csn_drive_root_id: str):
        """
        Initialize setup manager.

        Args:
            csn_drive_root_id: Root folder ID of CSN Shared Drive (Genomos)
        """
        self.csn_drive_root_id = csn_drive_root_id
        self.folder_ids = {"csn_shared_drive_root": csn_drive_root_id}

        # Initialize Google Drive Manager
        client_secret_file = os.getenv("GOOGLE_CLIENT_SECRET_FILE", "credentials/client_secret.json")
        token_file = os.getenv("GOOGLE_TOKEN_FILE", "credentials/token.json")

        logger.info(f"Initializing Google Drive Manager...")
        logger.info(f"  Client secret: {client_secret_file}")
        logger.info(f"  Token file: {token_file}")
        logger.info(f"  CSN Drive root: {csn_drive_root_id}")

        self.drive_manager = GoogleDriveManager(
            client_secret_file=client_secret_file,
            token_file=token_file,
            folder_id=csn_drive_root_id
        )

    def create_folder(
        self,
        folder_name: str,
        parent_id: str,
        description: str = ""
    ) -> str:
        """
        Create a folder in Google Drive.

        Args:
            folder_name: Name of folder to create
            parent_id: Parent folder ID
            description: Folder description (optional)

        Returns:
            Created folder ID
        """
        try:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_id]
            }

            if description:
                file_metadata['description'] = description

            folder = self.drive_manager.service.files().create(
                body=file_metadata,
                fields='id, name',
                supportsAllDrives=True  # Important for Shared Drives
            ).execute()

            folder_id = folder.get('id')
            logger.info(f"✅ Created folder: {folder_name} (ID: {folder_id})")

            return folder_id

        except Exception as e:
            logger.error(f"❌ Failed to create folder {folder_name}: {e}")
            raise

    def create_folder_structure(
        self,
        structure: Dict[str, Any],
        parent_id: str,
        path_prefix: str = ""
    ) -> Dict[str, str]:
        """
        Recursively create folder structure.

        Args:
            structure: Dict defining folder hierarchy
            parent_id: Parent folder ID
            path_prefix: Path prefix for tracking (e.g., "knowledge_base/voktere")

        Returns:
            Flat dict mapping path → folder_id
        """
        folder_mapping = {}

        for folder_name, config in structure.items():
            description = config.get("description", "")
            current_path = f"{path_prefix}/{folder_name}" if path_prefix else folder_name

            # Create folder
            folder_id = self.create_folder(folder_name, parent_id, description)
            folder_mapping[current_path] = folder_id

            # Recursively create subfolders
            subfolders = config.get("subfolders", {})
            if subfolders:
                subfolder_mapping = self.create_folder_structure(
                    subfolders,
                    folder_id,
                    current_path
                )
                folder_mapping.update(subfolder_mapping)

        return folder_mapping

    def setup(self) -> Dict[str, str]:
        """
        Setup complete CSN Knowledge Base folder structure.

        Returns:
            Complete folder ID mapping
        """
        logger.info("=" * 70)
        logger.info("CSN KNOWLEDGE BASE SETUP")
        logger.info("=" * 70)
        logger.info(f"Target: CSN Shared Drive (Genomos)")
        logger.info(f"Root folder ID: {self.csn_drive_root_id}")
        logger.info("")

        # Create main folder structure
        logger.info("Creating main folder structure...")
        folder_mapping = self.create_folder_structure(
            FOLDER_STRUCTURE,
            self.csn_drive_root_id
        )

        self.folder_ids.update(folder_mapping)

        logger.info("")
        logger.info("=" * 70)
        logger.info("SETUP COMPLETE")
        logger.info("=" * 70)
        logger.info(f"Total folders created: {len(folder_mapping)}")
        logger.info("")

        return self.folder_ids

    def save_folder_ids(self, output_file: str = "CSN_FOLDER_IDS.json"):
        """
        Save folder IDs to JSON file.

        Args:
            output_file: Output filename
        """
        output_path = Path(__file__).parent.parent / output_file

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.folder_ids, f, indent=2, ensure_ascii=False)

        logger.info(f"✅ Folder IDs saved to: {output_path}")

    def update_env_file(self):
        """
        Update .env file with folder IDs.
        """
        env_path = Path(__file__).parent.parent / ".env"

        # Key folder IDs to add to .env
        key_folders = {
            "CSN_SHARED_DRIVE_ROOT": self.csn_drive_root_id,
            "CSN_KNOWLEDGE_BASE_FOLDER_ID": self.folder_ids.get("01_Knowledge_Base"),
            "CSN_VOKTERE_FOLDER_ID": self.folder_ids.get("01_Knowledge_Base/voktere"),
            "CSN_DIMENSJONER_FOLDER_ID": self.folder_ids.get("01_Knowledge_Base/dimensjoner"),
            "CSN_PULSER_FOLDER_ID": self.folder_ids.get("01_Knowledge_Base/pulser"),
            "CSN_AGENT_COALITION_FOLDER_ID": self.folder_ids.get("02_Agent_Coalition"),
            "CSN_SMK_FOLDER_ID": self.folder_ids.get("03_SMK_Strategic_Docs"),
            "CSN_CHAPTERS_FOLDER_ID": self.folder_ids.get("04_Kompendium_Chapters"),
            "CSN_COLLABORATION_FOLDER_ID": self.folder_ids.get("05_Collaboration"),
        }

        # Read existing .env
        env_content = ""
        if env_path.exists():
            with open(env_path, 'r', encoding='utf-8') as f:
                env_content = f.read()

        # Append new variables (if not already present)
        lines_to_add = []
        for key, value in key_folders.items():
            if value and key not in env_content:
                lines_to_add.append(f"{key}={value}")

        if lines_to_add:
            with open(env_path, 'a', encoding='utf-8') as f:
                f.write("\n# CSN Knowledge Base Folder IDs (Auto-generated)\n")
                f.write("\n".join(lines_to_add))
                f.write("\n")

            logger.info(f"✅ Updated .env with {len(lines_to_add)} folder IDs")
        else:
            logger.info("ℹ️  .env already contains CSN folder IDs")

    def print_summary(self):
        """Print folder structure summary."""
        logger.info("")
        logger.info("=" * 70)
        logger.info("FOLDER STRUCTURE SUMMARY")
        logger.info("=" * 70)

        for path, folder_id in sorted(self.folder_ids.items()):
            indent = "  " * path.count("/")
            folder_name = path.split("/")[-1]
            logger.info(f"{indent}📁 {folder_name}")
            logger.info(f"{indent}   ID: {folder_id}")


def main():
    """Main setup execution."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Setup CSN Knowledge Base folder structure in Google Drive"
    )
    parser.add_argument(
        "--yes", "-y",
        action="store_true",
        help="Auto-approve folder creation without confirmation"
    )
    args = parser.parse_args()

    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    # Get CSN Shared Drive root ID from environment or prompt
    csn_drive_root_id = os.getenv("CSN_SHARED_DRIVE_ROOT")

    if not csn_drive_root_id:
        print("❌ CSN_SHARED_DRIVE_ROOT not found in .env")
        print("Please add to .env file:")
        print("  CSN_SHARED_DRIVE_ROOT=1SYTF7oUu8eVme_HdCvPQ5GFHCpRVe9E7")
        print("")

        # Prompt for manual entry
        csn_drive_root_id = input("Or enter CSN Shared Drive root folder ID now: ").strip()

        if not csn_drive_root_id:
            print("❌ No folder ID provided. Exiting.")
            sys.exit(1)

    # Confirm before creating
    print("")
    print("=" * 70)
    print("CSN KNOWLEDGE BASE SETUP")
    print("=" * 70)
    print(f"Target: CSN Shared Drive (Genomos)")
    print(f"Root folder ID: {csn_drive_root_id}")
    print("")
    print("This will create the following structure:")
    print("  01_Knowledge_Base/")
    print("    ├── voktere/ (5 category subfolders)")
    print("    ├── dimensjoner/ (3 grouping subfolders)")
    print("    └── pulser/")
    print("  02_Agent_Coalition/ (10 agent subfolders)")
    print("  03_SMK_Strategic_Docs/")
    print("  04_Kompendium_Chapters/")
    print("  05_Collaboration/")
    print("    ├── drafts/")
    print("    ├── reviews/")
    print("    └── archive/")
    print("")

    if not args.yes:
        confirm = input("Proceed with folder creation? (yes/no): ").strip().lower()

        if confirm not in ["yes", "y"]:
            print("❌ Setup cancelled.")
            sys.exit(0)
    else:
        print("✅ Auto-approved (--yes flag)")
        print("")

    # Run setup
    setup = CSNKnowledgeBaseSetup(csn_drive_root_id)
    folder_ids = setup.setup()

    # Save outputs
    setup.save_folder_ids()
    setup.update_env_file()
    setup.print_summary()

    print("")
    print("=" * 70)
    print("✅ CSN KNOWLEDGE BASE SETUP COMPLETE")
    print("=" * 70)
    print(f"Folders created: {len(folder_ids)}")
    print(f"Folder IDs saved: CSN_FOLDER_IDS.json")
    print(f".env updated with key folder IDs")
    print("")
    print("Next steps:")
    print("  1. Verify folder structure in CSN Drive (browser)")
    print("  2. Run: python scripts/extract_voktere.py")
    print("  3. Run: python scripts/sync_to_csn_drive.py")
    print("")


if __name__ == "__main__":
    main()
