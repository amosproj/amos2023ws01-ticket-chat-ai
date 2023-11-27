import json
import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import (
    AdamW,
    get_linear_schedule_with_warmup,
    T5ForConditionalGeneration,
    T5Tokenizer,
)
from tqdm import tqdm
import time


# Define your CustomDataset class
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
        target_json = json.dumps(
            self.target_jsons[idx]
        )  # Convert the dictionary to a JSON string

        inputs = self.tokenizer.encode_plus(
            "translate text to JSON: " + text_description,
            None,
            add_special_tokens=True,
            max_length=self.max_length,
            padding="max_length",
            return_token_type_ids=False,
            truncation=True,
            return_attention_mask=True,
            return_tensors="pt",
        )

        targets = self.tokenizer.encode_plus(
            target_json,
            None,
            add_special_tokens=True,
            max_length=self.max_length,
            padding="max_length",
            return_token_type_ids=False,
            truncation=True,
            return_attention_mask=True,
            return_tensors="pt",
        )

        return {
            "input_ids": inputs.input_ids.flatten(),
            "attention_mask": inputs.attention_mask.flatten(),
            "labels": targets.input_ids.flatten(),
        }


# Load the T5 model and tokenizer
model_name = "t5-small"
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

# Load prepared dataset
# Example: Replace this with your actual data loading
text_df = pd.read_csv("text.csv")
text_descriptions = text_df["text_description"].tolist()
target_jsons = [{"dummy": "data"}] * len(
    text_descriptions
)  # Replace with your actual target data

# Create datasets
train_dataset = CustomDataset(text_descriptions, target_jsons, tokenizer)
valid_dataset = CustomDataset(
    text_descriptions, target_jsons, tokenizer
)  # Replace with actual validation data

# Define data loaders
batch_size = 4
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
valid_loader = DataLoader(valid_dataset, batch_size=batch_size, shuffle=False)

# Hyperparameters
learning_rate = 1e-4
num_epochs = 4

# Optimizer and scheduler
optimizer = AdamW(model.parameters(), lr=learning_rate)
scheduler = get_linear_schedule_with_warmup(
    optimizer, num_warmup_steps=0, num_training_steps=len(train_loader) * num_epochs
)

# Check GPU availability
device = torch.device("cuda")
model.to(device)
if device.type == "cuda":
    print(f"Using GPU: {torch.cuda.get_device_name(0)}")
else:
    print("Using CPU")

# Training loop
for epoch in range(num_epochs):
    model.train()
    total_loss = 0
    start_time = time.time()

    for batch in tqdm(
        train_loader, desc=f"Epoch {epoch + 1}/{num_epochs}", unit="batch"
    ):
        optimizer.zero_grad()

        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        outputs = model(
            input_ids=input_ids, attention_mask=attention_mask, labels=labels
        )
        loss = outputs.loss
        total_loss += loss.item()
        loss.backward()
        optimizer.step()
        scheduler.step()

    average_loss = total_loss / len(train_loader)
    epoch_time = time.time() - start_time

    # Validation
    model.eval()
    total_accuracy = 0
    with torch.no_grad():
        for batch in valid_loader:
            # Add your validation logic here
            pass  # Replace this with actual accuracy calculation

    average_accuracy = total_accuracy / len(valid_loader)
    print(
        f"Epoch: {((epoch + 1) / num_epochs) * 100:.0f}% | {epoch + 1}/{num_epochs} [{epoch_time:.2f}s/epoch]"
    )
    print(f"Train Loss: {average_loss}")
    print(f"Validation Accuracy: {average_accuracy}")

# Save the fine-tuned model
model.save_pretrained("fine_tuned_t5_model")
tokenizer.save_pretrained("fine_tuned_t5_model")
