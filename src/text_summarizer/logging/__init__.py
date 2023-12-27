import os
import sys
import logging

logging_str = "[%(asctime)s: %(levelname)s: %(module)s:%(message)s]"
log_dir = os.path.abspath("D:\\projectFiles\\text_summarization_project\\research\\logs")  # Use absolute path for log directory
log_filename = "running_logs.log"

log_filepath = os.path.join(log_dir, log_filename)

os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=logging_str,

    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("textSummarizerLogger")
