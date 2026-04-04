from src.contextAwareSummarizationSystem.config.configuration import ConfigurationManager
from src.contextAwareSummarizationSystem.components.data_transformation import DataTransformation
from src.contextAwareSummarizationSystem.logging import logger

class DataTransformationPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            logger.info("Starting data transformation pipeline")
            config = ConfigurationManager()
            data_transformation_config = config.get_data_transformation_config()
            data_transformation = DataTransformation(config=data_transformation_config)
            data_transformation.convert()
            logger.info("Data transformation pipeline completed")
        except Exception as e:
            logger.error(f"Data transformation pipeline failed: {e}")
            raise e
