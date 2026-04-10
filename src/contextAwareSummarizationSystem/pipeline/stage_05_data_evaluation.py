from src.contextAwareSummarizationSystem.config.configuration import ConfigurationManager
from src.contextAwareSummarizationSystem.components.model_evaluation import ModelEvaluation
from src.contextAwareSummarizationSystem.logging import logger

class ModelEvaluationPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            logger.info("Starting model evaluation pipeline")
            config = ConfigurationManager()
            model_evaluation_config = config.get_model_evaluation_config()
            model_evaluation = ModelEvaluation(config=model_evaluation_config)
            model_evaluation.evaluate()
            logger.info("Model evaluation pipeline completed")
        except Exception as e:
            logger.error(f"Model evaluation pipeline failed: {e}")
            raise e
