import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

def get_log_file_path(log_dir, base_name="applogfile"):
    log_file = f"{base_name}.log"
    log_path = os.path.join(log_dir, log_file)
    return log_path

class CustomRotatingFileHandler(RotatingFileHandler):
    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None

        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        new_log_file = f"{self.baseFilename.rstrip('.log')}-{current_time}.log"

        if os.path.exists(self.baseFilename):
            os.rename(self.baseFilename, new_log_file)

        if not self.delay:
            self.stream = self._open()

def setup_logger(name, log_dir, max_bytes=1024*1024, backup_count=5, level=logging.INFO):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_path = get_log_file_path(log_dir)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(ch_formatter)

        # File handler
        fh = CustomRotatingFileHandler(log_path, maxBytes=max_bytes, backupCount=backup_count)
        fh.setLevel(logging.INFO)
        fh_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(fh_formatter)

        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger
