from dataclasses import dataclass
from pathlib import Path
from typing import List
@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir = Path
    source_url = str
    local_data_file = Path
    unzip_file = Path

@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    STATUS_FILE: Path
    ALL_REQUIRED_FILES: List[str]
    local_data_file: Path  
    unzip_dir: Path