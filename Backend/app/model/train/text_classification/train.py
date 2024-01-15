import argparse
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
        default=True,
        help="For Saving the current Model",
    )
    return parser.parse_args()


args = parse_args()

model_name = "roberta-base"
model = RobertaForSequenceClassification.from_pretrained(model_name)
tokenizer = RobertaTokenizer.from_pretrained(model_name)

root_directory = os.path.dirname(__file__)

test_dir = os.path.join(root_directory, "..", "test_data")
data_paths = [
    os.path.join(test_dir, "test_data_garvin", "data_translated.json"),
    os.path.join(test_dir, "test_data_irild", "data_translated.json"),
    os.path.join(test_dir, "test_data_fabian", "data_translated.json"),
    os.path.join(test_dir, "test_data_sajjad", "data_translated.json"),
    os.path.join(test_dir, "test_data_marco", "data_translated.json"),
    os.path.join(test_dir, "test_data_tino", "data_translated.json"),
    os.path.join(test_dir, "test_data_with_gpt", "data_1.json"),
    os.path.join(test_dir, "test_data_with_gpt", "data_2.json"),
    os.path.join(test_dir, "test_data_with_gpt", "test_data.json"),
]

# Create datasets
custom_dataset = CustomDataset(tokenizer, data_paths, "requestType")
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

    # Validation with Confusion Matrix
    model.eval()
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

    conf_matrix = confusion_matrix(val_true_labels, val_predictions)
    ax = sns.heatmap(conf_matrix, annot=True, cmap="Blues")

    ax.set_title("Confusion Matrix\n")
    ax.set_xlabel("\nPredicted Values")
    ax.set_ylabel("Actual Values ")

    ax.xaxis.set_ticklabels(["False", "True"])
    ax.yaxis.set_ticklabels(["False", "True"])

    # Save the confusion matrix plot as a PNG file
    plt.savefig(f"confusion_matrix_epoch_{epoch + 1}.png", bbox_inches="tight")
    plt.close()

    print(
        f"Epoch: {((epoch + 1) / args.epochs) * 100:.0f}% | {epoch + 1}/{args.epochs} [{epoch_time:.2f}s/epoch]"
    )
    print(f"Train Loss: {average_loss}")

# Save the fine-tuned model
if args.save_model:
    model.save_pretrained("fine_tuned_roberta_model")
    tokenizer.save_pretrained("fine_tuned_roberta_model")
