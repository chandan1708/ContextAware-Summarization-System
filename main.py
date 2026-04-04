from src.contextAwareSummarizationSystem.logging import logger
from src.contextAwareSummarizationSystem.pipeline.stage_01_data_ingestion import DataIngestionPipeline

try:
    logger.info("DataIngestion Stage Started")

    pipeline = DataIngestionPipeline()
    pipeline.main()
except Exception as e:
    logger.error(f"Error: {e}")