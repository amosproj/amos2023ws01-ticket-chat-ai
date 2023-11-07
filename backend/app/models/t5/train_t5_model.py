import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from torch.utils.data import DataLoader, Dataset
from transformers import AdamW, get_linear_schedule_with_warmup
import pandas as pd
import json

class CustomDataset(Dataset):
    def __init__(self, text_descriptions, target_jsons, tokenizer, max_length=512):
        self.text_descriptions = text_descriptions
        self.target_jsons = target_jsons
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.text_descriptions)

    def __getitem__(self, idx):
        text_description = self.text_descriptions[idx]
        target_json = json.dumps(self.target_jsons[idx])  # Convert the dictionary to a JSON string

        inputs = self.tokenizer.encode("translate text to JSON: " + text_description, return_tensors="pt", max_length=self.max_length, padding="max_length", truncation=True)
        targets = self.tokenizer.encode(target_json, return_tensors="pt", max_length=self.max_length, padding="max_length", truncation=True)

        return {
            "input_ids": inputs.view(-1),
            "attention_mask": (inputs != 0).view(-1),
            "labels": targets.view(-1),
        }

# Load the T5 model and tokenizer
model_name = "t5-small"
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

# Load prepared dataset
# Load descriptions from text.csv
text_df = pd.read_csv("text.csv")
text_descriptions = text_df["text_description"].tolist()

# Load JSON representations from tickets.json
with open("tickets.json", "r") as json_file:
    target_jsons = json.load(json_file)

# Create a CustomDataset
dataset = CustomDataset(text_descriptions, target_jsons, tokenizer)

# Define data loaders
batch_size = 4
train_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# Fine-tuning hyperparameters
learning_rate = 1e-4
num_epochs = 3

# Create the optimizer and learning rate scheduler
optimizer = AdamW(model.parameters(), lr=learning_rate)
scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=len(train_loader) * num_epochs)

print(torch.cuda.is_available())

# Training loop
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
model.to(device)

print("before epoch")
for epoch in range(num_epochs):
    model.train()
    total_loss = 0
    for batch in train_loader:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        optimizer.zero_grad()
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        scheduler.step()

        total_loss += loss.item()

    average_loss = total_loss / len(train_loader)
    print(f"Epoch {epoch + 1} | Average Loss: {average_loss}")

# Save the fine-tuned model
model.save_pretrained("fine_tuned_t5_model")
tokenizer.save_pretrained("fine_tuned_t5_model")

