from text_summarizer.constants import *

from text_summarizer.utils.common import read_yaml
from text_summarizer.utils.common import create_directories


from text_summarizer.entity import (DataIngestionConfig,DataValidationConfig)

from pathlib import Path

# Use absolute paths for configuration files
CONFIG_FILE_PATH = "D:\\projectFiles\\text_summarization_project\\config\\config.yaml"
PARAMS_FILE_PATH = "D:\\projectFiles\\text_summarization_project\\params.yaml"
from dataclasses import dataclass

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path
class ConfigurationManager:
    def __init__(
            self,
            config_filepath=Path(CONFIG_FILE_PATH),
            params_filepath=Path(PARAMS_FILE_PATH)):

        # Print the paths when initializing
        print("Config File Path:", config_filepath)
        print("Params File Path:", params_filepath)

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir
        )

        return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            STATUS_FILE=config.STATUS_FILE,
            ALL_REQUIRED_FILES=config.ALL_REQUIRED_FILES,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir
        )

        return data_validation_config
