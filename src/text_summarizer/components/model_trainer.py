import os 
from transformers import TrainingArguments,Trainer
from transformers import DataCollatorForSeq2Seq
from transformers import AutoModelForSeq2SeqLM,AutoTokenizer
from datasets import load_dataset,load_from_disk
import torch

from text_summarizer.entity import ModelTrainerConfig

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"

        # Use the specified model checkpoint
        model_checkpoint = "google/pegasus-xsum"
        model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(model_checkpoint, from_tf=True).to(device)

        # Initialize the tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

        seq2seq_data_collator = DataCollatorForSeq2Seq(tokenizer, model=model_pegasus)

        # loading data
        dataset_samsum_pt = load_from_disk(str(self.config.data_path))

        dataset_samsum_pt = dataset_samsum_pt.map(lambda example: {key: example[key][:10] for key in example})

        # Set the output directory to the desired path

        trainer_args = TrainingArguments(
            output_dir=self.config.root_dir,
            num_train_epochs=1,
            warmup_steps=50,
            per_device_train_batch_size=1,  # Reduce this value
            per_device_eval_batch_size=1,   # Reduce this value
            weight_decay=0.01,
            logging_steps=10,
            evaluation_strategy='steps',
            eval_steps=50,
            save_steps=1e6,
            gradient_accumulation_steps=16
        )


        trainer = Trainer(
            model=model_pegasus, args=trainer_args,
            tokenizer=tokenizer, data_collator=seq2seq_data_collator,
            train_dataset=dataset_samsum_pt["train"],
            eval_dataset=dataset_samsum_pt["validation"]
        )

        trainer.train()

        # Save model to the specified directory
        model_pegasus.save_pretrained(os.path.join(self.config.root_dir, "pegasus-samsum-model"))
        # Save tokenizer to the specified directory
        tokenizer.save_pretrained(os.path.join(self.config.root_dir, "tokenizer"))


