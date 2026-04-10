from src.contextAwareSummarizationSystem.logging import logger
from src.contextAwareSummarizationSystem.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from src.contextAwareSummarizationSystem.pipeline.stage_02_data_validation import DataValidationPipeline
from src.contextAwareSummarizationSystem.pipeline.stage_03_data_transformation import DataTransformationPipeline
from src.contextAwareSummarizationSystem.pipeline.stage_04_model_trainer import ModelTrainerPipeline
from src.contextAwareSummarizationSystem.pipeline.stage_05_data_evaluation import ModelEvaluationPipeline

try:
    logger.info("DataIngestion Stage Started")
    pipeline = DataIngestionPipeline()
    pipeline.main()
    logger.info("DataIngestion Stage Completed")
#--------------------------------------------------------------------------
    logger.info("DataValidation Stage Started")
    pipeline = DataValidationPipeline()
    pipeline.main()
    logger.info("DataValidation Stage Completed")

#--------------------------------------------------------------------------
    logger.info("Data Transformation Stage Started")
    pipeline = DataTransformationPipeline()
    pipeline.main()
    logger.info("Data Transformation Stage Completed")

#--------------------------------------------------------------------------
    logger.info("Model Trainer Stage Started")
    pipeline = ModelTrainerPipeline()
    pipeline.main()
    logger.info("Model Trainer Stage Completed")    

#--------------------------------------------------------------------------
    logger.info("Model Evaluation Stage Started")
    pipeline = ModelEvaluationPipeline()
    pipeline.main()
    logger.info("Model Evaluation Stage Completed")

except Exception as e:
    logger.error(f"Error: {e}")