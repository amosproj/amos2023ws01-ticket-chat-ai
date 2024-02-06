import argparse
import json
import os
import time
import torch
from torch.optim import AdamW
from torch.utils.data import DataLoader
from tqdm import tqdm
from transformers import RobertaForSequenceClassification, RobertaTokenizer
from transformers import get_linear_schedule_with_warmup
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import torch.nn.functional as F

from custom_data_set import CustomDataset


def parse_args():
    # input and output arguments
    parser = argparse.ArgumentParser(
        description="Train a neural network for text classification"
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=4,
        help="input batch size for training (default: 4)",
    )
    parser.add_argument(
        "--epochs", type=int, default=4, help="number of epochs to train (default: 4)"
    )
    parser.add_argument(
        "--lr", type=float, default=2e-5, help="learning rate (default: 0.00002)"
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
        default=True,
        help="For Saving the current Model",
    )
    parser.add_argument(
        "--classes",
        type=json.loads,  # Expect a JSON-formatted string for classes
        required=True,
        help='JSON-formatted string list of classes (e.g., \'["Class1", "Class2"]\')',
    )
    parser.add_argument(
        "--ticket_field",
        type=str,
        required=True,
        help="Field name for the ticket classification",
    )
    parser.add_argument(
        "--data_paths",
        type=json.loads,  # Expect a JSON-formatted string for data paths
        required=True,
        help='JSON-formatted string list of paths to training data (e.g., \'["path1", "path2"]\')',
    )
    return parser.parse_args()


args = parse_args()

###################
# <prepare the data>
###################

classes = args.classes
ticket_field = args.ticket_field
data_paths = args.data_paths

model_name = "roberta-base"
model = RobertaForSequenceClassification.from_pretrained(
    model_name, num_labels=len(classes)
)
tokenizer = RobertaTokenizer.from_pretrained(model_name)

root_directory = os.path.dirname(__file__)

# Create datasets
custom_dataset = CustomDataset(tokenizer, data_paths, ticket_field, classes)
train_set, val_set = torch.utils.data.random_split(
    custom_dataset,
    [
        int(len(custom_dataset) * 0.9),
        len(custom_dataset) - int(len(custom_dataset) * 0.9),
    ],
)

num_train_data = len(train_set)

##################
# <train the model>
##################

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

# Lists for learning curves
train_losses = []
valid_losses = []

# Training loop
for epoch in range(args.epochs):
    model.train()
    total_train_loss = 0

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
        total_train_loss += loss.item()
        loss.backward()
        optimizer.step()
        scheduler.step()

    average_train_loss = total_train_loss / len(train_loader)
    train_losses.append(average_train_loss)

    model.eval()
    total_valid_loss = 0
    val_true_labels = []
    val_predictions = []

    with torch.no_grad():
        for batch in valid_loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            preds = torch.argmax(logits, dim=1)

            val_true_labels.extend(labels.cpu().numpy())
            val_predictions.extend(preds.cpu().numpy())

            loss = torch.nn.functional.cross_entropy(logits, labels)
            total_valid_loss += loss.item()

    average_valid_loss = total_valid_loss / len(valid_loader)
    valid_losses.append(average_valid_loss)

    # Create and store confusion matrix
    conf_matrix = confusion_matrix(val_true_labels, val_predictions)
    plt.figure(figsize=(12, 8))
    ax = sns.heatmap(conf_matrix, annot=True, cmap="Blues")
    ax.set_title(f"Confusion Matrix for {ticket_field} \n")
    ax.set_xlabel("\nPredicted Values")
    ax.set_ylabel("Actual Values ")
    ax.set_xticklabels(classes, rotation=45, ha="right")
    ax.set_yticklabels(classes, rotation=45, ha="right")
    plt.savefig(
        f"confusion_matrix_epoch_{epoch + 1}" + ticket_field + ".png",
        bbox_inches="tight",
    )
    plt.close()

# Learning curves for training and validation loss
plt.figure(figsize=(10, 6))
plt.plot(train_losses, label="Training Loss")
plt.plot(valid_losses, label="Validation Loss")
plt.title(f"Loss of training and validation for {ticket_field} over the epochs")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()

# Save learning curve as an image
plt.savefig(f"training_validation_loss_curve_{ticket_field}.png")
plt.close()

# Save the fine-tuned model
if args.save_model:
    model.save_pretrained(
        "fine_tuned_roberta_model_" + ticket_field + str(num_train_data)
    )
    tokenizer.save_pretrained(
        "fine_tuned_roberta_model_" + ticket_field + str(num_train_data)
    )
