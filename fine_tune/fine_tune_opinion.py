import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset

# Modell und Tokenizer
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)  # Ja/Nein

# Dataset laden
dataset = load_dataset("csv", data_files="data/sentiment_train.csv")["train"]

# Opinion in Labels umwandeln (Yes=1, No=0)
def map_opinion(example):
    example["labels"] = 1 if example["opinion"] == "Yes" else 0
    return example

dataset = dataset.map(map_opinion)

# Tokenize
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

tokenized_dataset = dataset.map(tokenize_function, batched=True)
tokenized_dataset.set_format("torch", columns=["input_ids", "attention_mask", "labels"])

# Training-Argumente
training_args = TrainingArguments(
    output_dir="fine_tuned_opinion_model",
    num_train_epochs=15,
    per_device_train_batch_size=8,
    warmup_steps=50,
    weight_decay=0.05,
    logging_dir="logs",
    logging_steps=10,
    save_strategy="epoch",
    learning_rate=1e-5,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

# Training
trainer.train()

# Speichern
model.save_pretrained("fine_tuned_opinion_model")
tokenizer.save_pretrained("fine_tuned_opinion_model")
print("Fine-Tuning für Opinion Analyzer abgeschlossen!")