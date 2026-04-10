from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_dataset, load_from_disk
import evaluate
import torch
import os
import pandas as pd
from tqdm import tqdm
from src.contextAwareSummarizationSystem.logging import logger
from src.contextAwareSummarizationSystem.entity import ModelEvaluationConfig

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def _resolve_device(self) -> str:
        forced_device = os.getenv("FORCE_DEVICE", "").strip().lower()
        if forced_device in {"cuda", "mps", "cpu"}:
            logger.info(f"Using forced evaluation device from FORCE_DEVICE: {forced_device}")
            return forced_device

        if torch.cuda.is_available():
            return "cuda"
        if torch.backends.mps.is_available():
            return "mps"
        return "cpu"

    def generate_batch_sized_chunks(self,list_of_elements,batch_size):
        """
        Yield successive batch-sized chunks from list_of_elements.
        """
        for i in range(0, len(list_of_elements), batch_size):
            yield list_of_elements[i:i + batch_size]
    
    def calculate_metric_on_test_ds(self,dataset,metric,model,tokenizer,batch_size=16,device="cuda" if torch.cuda.is_available() else "cpu",column_text="article",column_summary="highlights"):
        article_batches = list(self.generate_batch_sized_chunks(dataset[column_text],batch_size))
        target_batches = list(self.generate_batch_sized_chunks(dataset[column_summary],batch_size))

        for article_batch,target_batch in tqdm(zip(article_batches,target_batches),total=len(article_batches)):
            inputs=tokenizer(article_batch,max_length=1024,truncation=True,padding="max_length",return_tensors="pt")
            summaries=model.generate(input_ids=inputs['input_ids'].to(device),attention_mask=inputs['attention_mask'].to(device),length_penalty=0.8,num_beams=4,max_length=128,early_stopping=True)

            decoded_summaries=[tokenizer.decode(s,skip_special_tokens=True,clean_up_tokenization_spaces=True) for s in summaries]
            metric.add_batch(predictions=decoded_summaries,references=target_batch)

        score=metric.compute()
        return score

    
    def evaluate(self):
        device = self._resolve_device()
        logger.info(f"Using device for evaluation: {device}")

        tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        model_pegasus=AutoModelForSeq2SeqLM.from_pretrained(self.config.model_path).to(device)

        dataset_samsum_pt=load_from_disk(self.config.data_path)

        rouge_names=["rouge1","rouge2","rougeL","rougeLsum"]
        rouge_metric=evaluate.load('rouge')
        eval_batch_size = 2 if device == "cuda" else 1
        score=self.calculate_metric_on_test_ds(dataset_samsum_pt['test'][0:10],rouge_metric,model_pegasus,tokenizer,batch_size=eval_batch_size,column_text="dialogue",column_summary="summary",device=device)
        rouge_dict=dict((rn,score[rn]) for rn in rouge_names)
        logger.info(f"ROUGE scores: {rouge_dict}")
        
        df=pd.DataFrame(rouge_dict,index=['pegasus'])
        df.to_csv(self.config.metric_file_name,index=False)
        logger.info(f"ROUGE scores saved to {self.config.metric_file_name}")
