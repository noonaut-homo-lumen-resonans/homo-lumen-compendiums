"""
Google Sheets Manager for GENOMOS Analytics

Logs consultations, patterns, and metrics to Google Sheets for:
- Real-time collaboration
- Easy visualization (charts, pivot tables)
- Accessible dashboards for non-technical Coalition members

Philosophy: "Blockchain for immutability + Sheets for collaboration"
"""

import gspread
from google.oauth2.credentials import Credentials
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)


class GoogleSheetsManager:
    """
    Manager for Google Sheets operations.

    Features:
    - Log consultations to Sheets
    - Log patterns to Sheets
    - Log agent activity
    - Log daily metrics
    - Append-only (preserves history)
    """

    def __init__(self, credentials: Credentials, spreadsheet_id: str):
        """
        Initialize Google Sheets Manager.

        Args:
            credentials: OAuth2 credentials (from GoogleDriveManager)
            spreadsheet_id: Google Sheets spreadsheet ID
        """
        self.spreadsheet_id = spreadsheet_id
        self.credentials = credentials

        # Initialize gspread client
        try:
            self.client = gspread.authorize(credentials)
            self.spreadsheet = self.client.open_by_key(spreadsheet_id)
            logger.info(f"✅ Connected to Google Sheets: {self.spreadsheet.title}")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Sheets: {e}")
            raise

        # Get sheet references
        self.consultations_sheet = self.spreadsheet.worksheet("Consultations")
        self.patterns_sheet = self.spreadsheet.worksheet("Patterns")
        self.agent_activity_sheet = self.spreadsheet.worksheet("Agent Activity")
        self.daily_metrics_sheet = self.spreadsheet.worksheet("Daily Metrics")

    def log_consultation(self, consultation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Log consultation to Sheets.

        Args:
            consultation_data: Consultation data from blockchain

        Returns:
            Status dict
        """
        try:
            # Extract data
            timestamp = datetime.now().isoformat()
            consultation_id = consultation_data.get("consultation_id", "N/A")
            question = consultation_data.get("human_query", "")[:500]  # Truncate
            agents = ", ".join(consultation_data.get("agents", []))
            smk_refs = ", ".join(consultation_data.get("related_smk", []))
            biofelt = "Yes" if consultation_data.get("biofelt_context") else "No"
            status = consultation_data.get("status", "completed")

            # Append row
            row = [timestamp, consultation_id, question, agents, smk_refs, biofelt, status]
            self.consultations_sheet.append_row(row)

            logger.info(f"✅ Logged consultation {consultation_id} to Sheets")

            return {
                "success": True,
                "consultation_id": consultation_id,
                "message": "Consultation logged to Google Sheets"
            }

        except Exception as e:
            logger.error(f"❌ Failed to log consultation: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to log consultation"
            }

    def log_pattern(self, pattern_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Log discovered pattern to Sheets.

        Args:
            pattern_data: Pattern data from Pattern Analyzer

        Returns:
            Status dict
        """
        try:
            # Extract data
            timestamp = datetime.now().isoformat()
            pattern_id = pattern_data.get("pattern_id", "N/A")
            pattern_type = pattern_data.get("pattern_type", "unknown")
            confidence = pattern_data.get("confidence", 0.0)
            description = pattern_data.get("description", "")[:500]
            data_json = json.dumps(pattern_data.get("data", {}))[:1000]

            # Append row
            row = [timestamp, pattern_id, pattern_type, confidence, description, data_json]
            self.patterns_sheet.append_row(row)

            logger.info(f"✅ Logged pattern {pattern_id} to Sheets")

            return {
                "success": True,
                "pattern_id": pattern_id,
                "message": "Pattern logged to Google Sheets"
            }

        except Exception as e:
            logger.error(f"❌ Failed to log pattern: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to log pattern"
            }

    def update_agent_activity(self, agent_stats: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Update agent activity dashboard.

        Args:
            agent_stats: List of agent statistics

        Returns:
            Status dict
        """
        try:
            # Clear existing data (keep headers)
            self.agent_activity_sheet.clear()

            # Add headers
            headers = ["Agent", "Total Genes", "SMK Count", "Mutation Count", "Last Activity"]
            self.agent_activity_sheet.append_row(headers)

            # Add agent data
            for stats in agent_stats:
                row = [
                    stats.get("agent", "unknown"),
                    stats.get("total_genes", 0),
                    stats.get("smk_count", 0),
                    stats.get("mutation_count", 0),
                    stats.get("last_activity", "N/A")
                ]
                self.agent_activity_sheet.append_row(row)

            logger.info(f"✅ Updated agent activity ({len(agent_stats)} agents)")

            return {
                "success": True,
                "agents_updated": len(agent_stats),
                "message": "Agent activity updated in Google Sheets"
            }

        except Exception as e:
            logger.error(f"❌ Failed to update agent activity: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to update agent activity"
            }

    def log_daily_metrics(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Log daily metrics.

        Args:
            metrics: Daily metrics from blockchain

        Returns:
            Status dict
        """
        try:
            # Extract data
            date = datetime.now().strftime("%Y-%m-%d")
            total_blocks = metrics.get("total_blocks", 0)
            new_consultations = metrics.get("new_consultations", 0)
            new_patterns = metrics.get("new_patterns", 0)
            active_agents = metrics.get("active_agents", 0)

            # Append row
            row = [date, total_blocks, new_consultations, new_patterns, active_agents]
            self.daily_metrics_sheet.append_row(row)

            logger.info(f"✅ Logged daily metrics for {date}")

            return {
                "success": True,
                "date": date,
                "message": "Daily metrics logged to Google Sheets"
            }

        except Exception as e:
            logger.error(f"❌ Failed to log daily metrics: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to log daily metrics"
            }

    def get_sheet_url(self) -> str:
        """Get URL to Google Sheets workbook."""
        return f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}"

    def verify_connection(self) -> Dict[str, Any]:
        """
        Verify connection to Google Sheets.

        Returns:
            Status dict
        """
        try:
            title = self.spreadsheet.title
            url = self.get_sheet_url()

            return {
                "connected": True,
                "spreadsheet_title": title,
                "spreadsheet_id": self.spreadsheet_id,
                "url": url,
                "message": "Google Sheets connection verified"
            }

        except Exception as e:
            logger.error(f"❌ Sheets connection failed: {e}")
            return {
                "connected": False,
                "error": str(e),
                "message": "Failed to connect to Google Sheets"
            }


# Global instance (initialized by main.py)
_sheets_manager: Optional[GoogleSheetsManager] = None


def initialize_sheets_manager(
    credentials: Credentials,
    spreadsheet_id: str
) -> GoogleSheetsManager:
    """Initialize global GoogleSheetsManager instance."""
    global _sheets_manager
    _sheets_manager = GoogleSheetsManager(credentials, spreadsheet_id)
    return _sheets_manager


def get_sheets_manager() -> Optional[GoogleSheetsManager]:
    """Get global GoogleSheetsManager instance."""
    return _sheets_manager