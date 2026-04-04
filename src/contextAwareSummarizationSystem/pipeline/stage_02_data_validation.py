from src.contextAwareSummarizationSystem.config.configuration import ConfigurationManager
from src.contextAwareSummarizationSystem.components.data_validation import DataValidation
from src.contextAwareSummarizationSystem.logging import logger

class DataValidationPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            logger.info("Starting data validation pipeline")
            config = ConfigurationManager()
            data_validation_config = config.get_data_validation_config()
            data_validation = DataValidation(config=data_validation_config)
            data_validation.validate_all_files_exist()
            logger.info("Data validation pipeline completed")
        except Exception as e:
            logger.error(f"Data validation pipeline failed: {e}")
            raise e

