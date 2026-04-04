import os
from src.contextAwareSummarizationSystem.logging import logger
from src.contextAwareSummarizationSystem.entity import DataValidationConfig

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_files_exist(self):
        try:
            validation_status = True

            all_files=os.listdir(os.path.join("artifacts","data_ingestion","samsum_dataset"))

            for required_file in self.config.ALL_REQUIRED_FILES:
                if required_file not in all_files:
                    validation_status = False
                    break

            with open(self.config.STATUS_FILE,'w') as f:
                f.write(f"Validation status: {validation_status}")

            logger.info(f"Validation status: {validation_status}")
        except Exception as e:
            logger.error(f"Data validation failed: {e}")
            raise e