from transformers import TrainingArguments, Trainer 
from transformers import DataCollatorForSeq2Seq
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_dataset, load_from_disk
import torch 
import os
from src.contextAwareSummarizationSystem.logging import logger
from src.contextAwareSummarizationSystem.entity import ModelTrainerConfig

class ModelTrainer:
    def __init__(self, config:ModelTrainerConfig):
        self.config = config

    def train(self):
        os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
        os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"

        if torch.cuda.is_available():
            device = "cuda"
        elif torch.backends.mps.is_available():
            device = "mps"
        else:
            device = "cpu"
        logger.info(f"Using device for training: {device}")

        tokenizer=AutoTokenizer.from_pretrained(self.config.model_ckpt)
        model_pegasus=AutoModelForSeq2SeqLM.from_pretrained(self.config.model_ckpt).to(device)
        seq2seq_data_collator=DataCollatorForSeq2Seq(tokenizer, model=model_pegasus)

        # Load dataset
        dataset_samsum_pt = load_from_disk(self.config.data_path)

        training_args=TrainingArguments(
            output_dir=self.config.root_dir,
            num_train_epochs=self.config.num_train_epochs,
            warmup_steps=self.config.warmup_steps,
            per_device_train_batch_size=self.config.per_device_train_batch_size,
            weight_decay=self.config.weight_decay,
            logging_steps=self.config.logging_steps,
            evaluation_strategy=self.config.evaluation_strategy,
            eval_steps=self.config.eval_steps,
            save_steps=self.config.save_steps,
            gradient_accumulation_steps=self.config.gradient_accumulation_steps,
            fp16=(device == "cuda"),
            dataloader_pin_memory=False,
            report_to=[],
            save_total_limit=1
        )
        trainer=Trainer(
            model=model_pegasus,
            args=training_args,
            train_dataset=dataset_samsum_pt["train"],
            eval_dataset=dataset_samsum_pt["validation"],
            data_collator=seq2seq_data_collator,
            tokenizer=tokenizer
        )
        trainer.train()

        model_pegasus.save_pretrained(os.path.join(self.config.root_dir,"pegasus-samsum-model"))
        tokenizer.save_pretrained(os.path.join(self.config.root_dir,"tokenizer"))

        logger.info("Model training completed")