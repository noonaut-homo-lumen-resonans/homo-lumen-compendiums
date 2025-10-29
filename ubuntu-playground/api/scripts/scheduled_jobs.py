"""
Scheduled Jobs for GENOMOS

Automated tasks:
1. Daily backup to Google Drive (2 AM default)
2. Pattern analysis every 6 hours
3. Daily metrics logging to Google Sheets

Philosophy: "The genome maintains itself"
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)


class GenomosScheduler:
    """
    Manages scheduled jobs for GENOMOS.

    Features:
    - Daily Google Drive backup
    - Periodic pattern analysis
    - Daily metrics logging
    - Background execution (non-blocking)
    """

    def __init__(
        self,
        blockchain,
        drive_manager,
        sheets_manager,
        backup_hour: int = 2,
        pattern_interval_hours: int = 6
    ):
        """
        Initialize scheduler.

        Args:
            blockchain: AgentDNAChain instance
            drive_manager: GoogleDriveManager instance
            sheets_manager: GoogleSheetsManager instance
            backup_hour: Hour of day for daily backup (0-23)
            pattern_interval_hours: Hours between pattern analysis
        """
        self.blockchain = blockchain
        self.drive_manager = drive_manager
        self.sheets_manager = sheets_manager
        self.backup_hour = backup_hour
        self.pattern_interval_hours = pattern_interval_hours

        # Create scheduler
        self.scheduler = BackgroundScheduler()
        self.jobs_registered = []

    def start(self):
        """Start scheduler and register jobs."""
        logger.info("🕐 Starting GENOMOS scheduler...")

        # Job 1: Daily backup to Google Drive
        self.scheduler.add_job(
            func=self._daily_backup_job,
            trigger=CronTrigger(hour=self.backup_hour, minute=0),
            id="daily_backup",
            name="Daily Google Drive Backup",
            replace_existing=True
        )
        self.jobs_registered.append("daily_backup")
        logger.info(f"✅ Registered: Daily backup at {self.backup_hour}:00")

        # Job 2: Pattern analysis (every N hours)
        self.scheduler.add_job(
            func=self._pattern_analysis_job,
            trigger=IntervalTrigger(hours=self.pattern_interval_hours),
            id="pattern_analysis",
            name="Pattern Analysis",
            replace_existing=True
        )
        self.jobs_registered.append("pattern_analysis")
        logger.info(f"✅ Registered: Pattern analysis every {self.pattern_interval_hours} hours")

        # Job 3: Daily metrics logging
        self.scheduler.add_job(
            func=self._daily_metrics_job,
            trigger=CronTrigger(hour=23, minute=55),  # End of day
            id="daily_metrics",
            name="Daily Metrics Logging",
            replace_existing=True
        )
        self.jobs_registered.append("daily_metrics")
        logger.info("✅ Registered: Daily metrics at 23:55")

        # Start scheduler
        self.scheduler.start()
        logger.info(f"🚀 Scheduler started with {len(self.jobs_registered)} jobs")

    def stop(self):
        """Stop scheduler."""
        self.scheduler.shutdown(wait=False)
        logger.info("🛑 Scheduler stopped")

    def _daily_backup_job(self):
        """
        Job 1: Create backup and upload to Google Drive.
        """
        try:
            logger.info("📦 Starting daily backup job...")

            # Import here to avoid circular imports
            from blockchain.backup_manager import BackupManager

            backup_mgr = BackupManager(self.blockchain)

            # Create backup with Drive upload
            result = backup_mgr.create_backup_with_drive(self.drive_manager)

            if result.get("success"):
                logger.info(f"✅ Backup completed: {result['backup_file']}")
                logger.info(f"☁️ Uploaded to Drive: {result.get('drive_upload', {}).get('file_id', 'N/A')}")
            else:
                logger.error(f"❌ Backup failed: {result.get('error', 'Unknown error')}")

        except Exception as e:
            logger.error(f"❌ Daily backup job failed: {e}")

    def _pattern_analysis_job(self):
        """
        Job 2: Analyze blockchain for patterns.
        """
        try:
            logger.info("🔍 Starting pattern analysis job...")

            # Import here to avoid circular imports
            from blockchain.pattern_analyzer import PatternAnalyzer
            from blockchain.dna_block import GeneType

            analyzer = PatternAnalyzer(self.blockchain)

            # Run analysis
            patterns = analyzer.analyze_all(min_confidence=0.5, lookback_days=30)

            if patterns:
                logger.info(f"✅ Found {len(patterns)} patterns")

                # Store patterns in blockchain
                for pattern in patterns:
                    try:
                        pattern_gene = self.blockchain.add_gene(
                            gene_type=GeneType.PATTERN,
                            data=pattern,
                            agent="pattern-analyzer",
                            tags=["pattern", pattern["pattern_type"], "automated"]
                        )
                        logger.info(f"💾 Stored pattern {pattern['pattern_id']} as block #{pattern_gene.index}")

                        # Log to Google Sheets
                        self.sheets_manager.log_pattern(pattern)

                    except Exception as e:
                        logger.error(f"❌ Failed to store pattern {pattern.get('pattern_id')}: {e}")

                logger.info(f"✅ Pattern analysis complete: {len(patterns)} patterns stored")
            else:
                logger.info("ℹ️ No new patterns detected")

        except Exception as e:
            logger.error(f"❌ Pattern analysis job failed: {e}")

    def _daily_metrics_job(self):
        """
        Job 3: Log daily metrics to Google Sheets.
        """
        try:
            logger.info("📊 Starting daily metrics job...")

            # Get blockchain info
            chain_info = self.blockchain.get_chain_info()

            # Count consultations and patterns from today
            from datetime import date
            today = date.today().isoformat()

            consultations_today = [
                b for b in self.blockchain.get_genes_by_type("consultation")
                if b.timestamp.startswith(today)
            ]

            patterns_today = [
                b for b in self.blockchain.get_genes_by_type("pattern")
                if b.timestamp.startswith(today)
            ]

            # Count unique agents active today
            agents_today = set()
            for b in self.blockchain.get_all_blocks():
                if b.timestamp.startswith(today) and hasattr(b, 'agent'):
                    agents_today.add(b.agent)

            # Prepare metrics
            metrics = {
                "total_blocks": chain_info.get("total_blocks", 0),
                "new_consultations": len(consultations_today),
                "new_patterns": len(patterns_today),
                "active_agents": len(agents_today)
            }

            # Log to Google Sheets
            result = self.sheets_manager.log_daily_metrics(metrics)

            if result.get("success"):
                logger.info(f"✅ Daily metrics logged: {metrics}")
            else:
                logger.error(f"❌ Failed to log metrics: {result.get('error')}")

        except Exception as e:
            logger.error(f"❌ Daily metrics job failed: {e}")

    def get_jobs_status(self):
        """Get status of all scheduled jobs."""
        jobs_status = []

        for job in self.scheduler.get_jobs():
            jobs_status.append({
                "id": job.id,
                "name": job.name,
                "next_run": job.next_run_time.isoformat() if job.next_run_time else None,
                "trigger": str(job.trigger)
            })

        return {
            "scheduler_running": self.scheduler.running,
            "total_jobs": len(jobs_status),
            "jobs": jobs_status
        }

    def run_job_now(self, job_id: str):
        """
        Manually trigger a job.

        Args:
            job_id: Job ID (daily_backup, pattern_analysis, daily_metrics)
        """
        job_map = {
            "daily_backup": self._daily_backup_job,
            "pattern_analysis": self._pattern_analysis_job,
            "daily_metrics": self._daily_metrics_job
        }

        if job_id in job_map:
            logger.info(f"▶️ Manually triggering job: {job_id}")
            job_map[job_id]()
            return {"success": True, "job_id": job_id, "message": f"Job {job_id} executed"}
        else:
            return {"success": False, "error": f"Unknown job: {job_id}"}


# Global scheduler instance
_scheduler: GenomosScheduler = None


def initialize_scheduler(
    blockchain,
    drive_manager,
    sheets_manager,
    backup_hour: int = None,
    pattern_interval_hours: int = None
):
    """
    Initialize global scheduler.

    Args:
        blockchain: AgentDNAChain instance
        drive_manager: GoogleDriveManager instance
        sheets_manager: GoogleSheetsManager instance
        backup_hour: Hour for daily backup (default from env)
        pattern_interval_hours: Interval for pattern analysis (default from env)
    """
    global _scheduler

    # Get config from environment
    if backup_hour is None:
        backup_hour = int(os.getenv("BACKUP_SCHEDULE_HOUR", "2"))

    if pattern_interval_hours is None:
        pattern_interval_hours = int(os.getenv("PATTERN_ANALYSIS_INTERVAL_HOURS", "6"))

    _scheduler = GenomosScheduler(
        blockchain,
        drive_manager,
        sheets_manager,
        backup_hour,
        pattern_interval_hours
    )

    _scheduler.start()

    return _scheduler


def get_scheduler():
    """Get global scheduler instance."""
    return _scheduler
