import logging
from logging.handlers import TimedRotatingFileHandler
import os
import zipfile
from datetime import datetime


class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, when, interval, backupCount, backup_dir, **kwargs):
        # Ensure the log directory exists
        log_dir = os.path.dirname(filename)
        os.makedirs(log_dir, exist_ok=True)

        # Ensure the backup directory exists
        os.makedirs(backup_dir, exist_ok=True)

        super().__init__(filename, when, interval, backupCount, **kwargs)
        self.backup_dir = backup_dir

    def doRollover(self):
        # Perform the normal rollover
        super().doRollover()

        # Move old logs to the backup directory and compress them
        zip_name = os.path.join(
            self.backup_dir, f"logs_backup_{datetime.now().strftime('%Y-%m')}.zip"
        )

        with zipfile.ZipFile(zip_name, "a", zipfile.ZIP_DEFLATED) as zipf:
            log_dir = os.path.dirname(self.baseFilename)
            for log_file in os.listdir(log_dir):
                log_file_path = os.path.join(log_dir, log_file)

                # Check if the file is a rolled-over log file
                if (
                    log_file.startswith(os.path.basename(self.baseFilename))
                    and log_file != os.path.basename(self.baseFilename)
                ):
                    zipf.write(log_file_path, os.path.basename(log_file_path))
                    os.remove(log_file_path)
