from src.contextAwareSummarizationSystem.config.configuration import ConfigurationManager
from src.contextAwareSummarizationSystem.components.model_tranier import ModelTrainer
from src.contextAwareSummarizationSystem.logging import logger

class ModelTrainerPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            logger.info("Starting model trainer pipeline")
            config = ConfigurationManager()
            model_trainer_config = config.get_model_trainer_config()
            model_trainer = ModelTrainer(config=model_trainer_config)
            model_trainer.train()
            logger.info("Model trainer pipeline completed")
        except Exception as e:
            logger.error(f"Model trainer pipeline failed: {e}")
            raise e
