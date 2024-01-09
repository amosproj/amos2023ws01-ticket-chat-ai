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
    parser.add_argument(
        "--accumulation_steps",  # Add this line for gradient accumulation
        type=int,
        default=1,
        help="number of steps for gradient accumulation (default: 1)",
    )
    parser.add_argument(
        "--no_cuda", action="store_true", default=False, help="disables CUDA training"
    )
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

model_name = "t5-base"
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

# Ensure the model is on the correct device before DataParallel
device = "cuda" if not args.no_cuda and torch.cuda.is_available() else "cpu"
model = model.to(device)

# Use DataParallel to distribute the model across multiple GPUs
if torch.cuda.device_count() > 1:
    print(f"Using {torch.cuda.device_count()} GPUs for DataParallel.")
    model = torch.nn.DataParallel(model)
root_directory = os.path.dirname(__file__)

test_dir = os.path.join(root_directory, "..", "data")
data_path = os.path.join(test_dir, "text_and_tickets.csv")
prompt_path = os.path.join(root_directory, "prompt.txt")

custom_dataset = CustomDataset(tokenizer, data_path, prompt_path)
train_set, val_set = torch.utils.data.random_split(
    custom_dataset,
    [
        int(len(custom_dataset) * 0.9),
        len(custom_dataset) - int(len(custom_dataset) * 0.9),
    ],
)

train_loader = DataLoader(train_set, batch_size=args.batch_size, shuffle=True)
valid_loader = DataLoader(val_set, batch_size=args.batch_size, shuffle=False)

optimizer = AdamW(model.parameters(), lr=args.lr)
scheduler = get_linear_schedule_with_warmup(
    optimizer, num_warmup_steps=0, num_training_steps=len(train_loader) * args.epochs
)

# No need to move the model to the device, DataParallel handles it internally

for epoch in range(args.epochs):
    model.train()
    total_loss = 0
    start_time = time.time()

    for batch_num, batch in enumerate(
        tqdm(train_loader, desc=f"Epoch {epoch + 1}/{args.epochs}", unit="batch")
    ):
        optimizer.zero_grad()

        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        outputs = model(
            input_ids=input_ids, attention_mask=attention_mask, labels=labels
        )
        loss = outputs.loss

        if loss.numel() == 1:  # Check if loss is a scalar tensor
            total_loss += loss.item()
        else:
            total_loss += loss.sum().item()

        # print(f"Batch: {batch_num + 1}, Loss Shape: {loss.shape}, Loss Value: {loss.item() if loss.numel() == 1 else loss}")

        # Backward pass
        if loss.numel() == 1:  # Check if loss is a scalar tensor
            loss.backward()
        else:
            loss.sum().backward()

        if (batch_num + 1) % args.accumulation_steps == 0:
            optimizer.step()
            optimizer.zero_grad()
            scheduler.step()

    average_loss = total_loss / len(train_loader)
    epoch_time = time.time() - start_time

    # Validation
    model.eval()
    total_accuracy = 0
    with torch.no_grad():
        for batch in valid_loader:
            pass

    average_accuracy = total_accuracy / len(valid_loader)
    print(
        f"Epoch: {((epoch + 1) / args.epochs) * 100:.0f}% | {epoch + 1}/{args.epochs} [{epoch_time:.2f}s/epoch]"
    )
    print(f"Train Loss: {average_loss}")
    print(f"Validation Accuracy: {average_accuracy}")

# Save the fine-tuned model
# if args.save_model:
# Assuming 'model' is wrapped with DataParallel
if isinstance(model, torch.nn.DataParallel):
    model_to_save = model.module  # Extract the underlying model
else:
    model_to_save = model

# Save the pretrained model
model_to_save.save_pretrained("fine_tuned_t5_model")
tokenizer.save_pretrained("fine_tuned_t5_model")
