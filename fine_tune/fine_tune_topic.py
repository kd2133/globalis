import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset

# Modell und Tokenizer
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=6)  # 6 Topics!
# Dataset laden
dataset = load_dataset("csv", data_files="data/sentiment_train.csv")["train"]

# Themen in Labels umwandeln
topic_map = {
    "Migration": 0,
    "Environment": 1,
    "Safety": 2,
    "Energy": 3,
    "Inflation": 4,
    "Other": 5
}
def map_topic(example):
    if example["topic"] in topic_map:
        example["labels"] = topic_map[example["topic"]]
    else:
        print(f"Unknown topic: {example['topic']}")
        example["labels"] = -1
    return example

dataset = dataset.map(map_topic)
dataset = dataset.filter(lambda x: x["labels"] != -1)

# Shuffle-Datensatz
dataset = dataset.shuffle(seed=42)  # Seed für reproduzierbare Ergebnisse

# Tokenize
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

tokenized_dataset = dataset.map(tokenize_function, batched=True)
tokenized_dataset.set_format("torch", columns=["input_ids", "attention_mask", "labels"])

# Training-Argumente
training_args = TrainingArguments(
    output_dir="fine_tuned_topic_model",
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
model.save_pretrained("fine_tuned_topic_model")
tokenizer.save_pretrained("fine_tuned_topic_model")
print("Fine-Tuning für Topic Analyzer abgeschlossen!")

# ---- Confusion Matrix nach dem Training ----
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Beispiel: Nutze die ersten 50 Beispiele als "Test" (besser wäre ein echter Val/Test-Split!)
test_dataset = tokenized_dataset.select(range(0, 50))

# Vorhersagen erzeugen
preds = trainer.predict(test_dataset)
y_true = preds.label_ids
y_pred = preds.predictions.argmax(axis=1)

labels = ["Migration", "Environment", "Safety", "Energy", "Inflation", "Other"]
cm = confusion_matrix(y_true, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
disp.plot(cmap="Blues", xticks_rotation=45)
plt.show()

# Accuracy berechnen und ausgeben
accuracy = (y_true == y_pred).mean()
print(f"Accuracy auf Test-Subset: {accuracy:.2f}")