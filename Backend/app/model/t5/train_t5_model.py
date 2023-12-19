import argparse
import os
import time

import torch
from torch.optim import AdamW
from torch.utils.data import DataLoader
from tqdm import tqdm
from transformers import (
    get_linear_schedule_with_warmup,
    T5ForConditionalGeneration,
    T5Tokenizer,
)

# Define your CustomDataset class
# Load the T5 model and tokenizer
from custom_data_set import CustomDataset


def parse_args():
    parser = argparse.ArgumentParser(
        description="Train a neural network to diffuse images"
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=4,
        help="input batch size for training (default: 64)",
    )
    parser.add_argument(
        "--epochs", type=int, default=4, help="number of epochs to train (default: 5)"
    )
    parser.add_argument(
        "--lr", type=float, default=2e-5, help="learning rate (default: 0.003)"
    )
    # parser.add_argument('--momentum', type=float, default=0.9, help='SGD momentum (default: 0.9)')
    parser.add_argument(
        "--no_cuda", action="store_true", default=False, help="disables CUDA training"
    )
    # parser.add_argument('--seed', type=int, default=1, help='random seed (default: 1)')
    parser.add_argument(
        "--log_interval",
        type=int,
        default=100,
        help="how many batches to wait before logging training status",
    )
    parser.add_argument(
        "--save_model",
        action="store_true",
        default=False,
        help="For Saving the current Model",
    )
    return parser.parse_args()


args = parse_args()

model_name = "t5-small"
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

root_directory = os.path.dirname(__file__)

test_dir = os.path.join(root_directory, "..", "test_data")
data_paths = [
    os.path.join(test_dir, "test_data_garvin", "data.json"),
    os.path.join(test_dir, "test_data_irild", "data.json"),
    os.path.join(test_dir, "test_data_marco", "data.json"),
    os.path.join(test_dir, "test_data_sajjad", "data.json"),
    os.path.join(test_dir, "test_data_tino", "data.json"),
]

prompt_path = os.path.join(root_directory, "prompt.txt")

# Create datasets
custom_dataset = CustomDataset(tokenizer, data_paths, prompt_path)
train_set, val_set = torch.utils.data.random_split(
    custom_dataset,
    [
        int(len(custom_dataset) * 0.9),
        len(custom_dataset) - int(len(custom_dataset) * 0.9),
    ],
)

# Define data loaders
train_loader = DataLoader(train_set, batch_size=args.batch_size, shuffle=True)
valid_loader = DataLoader(val_set, batch_size=args.batch_size, shuffle=False)

# Optimizer and scheduler
optimizer = AdamW(model.parameters(), lr=args.lr)
scheduler = get_linear_schedule_with_warmup(
    optimizer, num_warmup_steps=0, num_training_steps=len(train_loader) * args.epochs
)

# Check GPU availability
device = "cuda" if not args.no_cuda and torch.cuda.is_available() else "cpu"
model.to(device)

# Training loop
for epoch in range(args.epochs):
    model.train()
    total_loss = 0
    start_time = time.time()

    for batch in tqdm(
        train_loader, desc=f"Epoch {epoch + 1}/{args.epochs}", unit="batch"
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
            # input_ids = batch["input_ids"].to(device)
            # attention_mask = batch["attention_mask"].to(device)
            # labels = batch["labels"].to(device)
            #
            # outputs = model(
            #     input_ids=input_ids, attention_mask=attention_mask, labels=labels
            # )
            # # Add your validation logic here
            # total_accuracy += outputs.eq(labels).sum().item()  # Replace this with actual accuracy calculation
            pass

    average_accuracy = total_accuracy / len(valid_loader)
    print(
        f"Epoch: {((epoch + 1) / args.epochs) * 100:.0f}% | {epoch + 1}/{args.epochs} [{epoch_time:.2f}s/epoch]"
    )
    print(f"Train Loss: {average_loss}")
    print(f"Validation Accuracy: {average_accuracy}")

# Save the fine-tuned model
if args.save_model:
    model.save_pretrained("fine_tuned_t5_model")
    tokenizer.save_pretrained("fine_tuned_t5_model")
