import os
from src.contextAwareSummarizationSystem.logging import logger
from datasets import load_dataset, load_from_disk
from transformers import AutoTokenizer
from src.contextAwareSummarizationSystem.entity import DataTransformationConfig

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(config.tokenizer_name)

    def convert_examples_to_features(self,example_batch):
    # The new way is to pass the target labels into the 'text_target' parameter natively
        encodings = self.tokenizer(
            text=example_batch['dialogue'], 
            text_target=example_batch['summary'], 
            max_length=1024, 
            truncation=True
        )
        
        return {
            'input_ids': encodings['input_ids'],
            'attention_mask': encodings['attention_mask'],
            'labels': encodings['labels']
        }

    def convert(self):
        dataset_samsum = load_from_disk(self.config.data_path)
        dataset_samsum_pt = dataset_samsum.map(self.convert_examples_to_features, batched=True)
        dataset_samsum_pt.save_to_disk(os.path.join(self.config.root_dir,"samsum_dataset"))
        logger.info("Data transformation completed")