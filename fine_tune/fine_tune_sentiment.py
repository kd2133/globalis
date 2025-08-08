from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset

# Modell und Tokenizer laden
model_name = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=1,
    problem_type="regression",
    ignore_mismatched_sizes=True
)

# Datensatz laden und Labels als float setzen
dataset = load_dataset("csv", data_files="data/sentiment_train.csv")["train"]
dataset = dataset.map(lambda x: {"sentiment": float(x["sentiment"])}, batched=False)

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

tokenized_dataset = dataset.map(tokenize_function, batched=True)
tokenized_dataset = tokenized_dataset.rename_column("sentiment", "labels")
tokenized_dataset.set_format("torch", columns=["input_ids", "attention_mask", "labels"])

training_args = TrainingArguments(
    output_dir="fine_tuned_model",
    num_train_epochs=15,
    per_device_train_batch_size=8,
    warmup_steps=50,
    weight_decay=0.05,
    logging_dir="logs",
    logging_steps=10,
    save_strategy="epoch",
    learning_rate=1e-5,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

trainer.train()
model.save_pretrained("fine_tuned_model")
tokenizer.save_pretrained("fine_tuned_model")
print("Fine-Tuning abgeschlossen!")