from src.contextAwareSummarizationSystem.config.configuration import ConfigurationManager
from src.contextAwareSummarizationSystem.components.data_ingestion import DataIngestion
from src.contextAwareSummarizationSystem.logging import logger

class DataIngestionPipeline:
    def __init__(self):
        pass

    def main(self):
        logger.info("Starting data ingestion pipeline")
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.download_file()
        data_ingestion.extract_file()
        logger.info("Data ingestion pipeline completed")