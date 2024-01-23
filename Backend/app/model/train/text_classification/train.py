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
import torch.nn.functional as F

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

# classes = ["Incident", "Service Request"]
# ticket_field = "requestType"
# classes = ['SAP ERP', 'Atlassian', 'Adobe', 'Salesforce', 'Reporting', 'Microsoft Power Platform', 'Microsoft SharePoint', 'Snowflake', 'Microsoft Office']
# ticket_field = "service"
classes = [
    "HANA -> Technical Issues",
    "HANA -> Billing & Payment",
    "HANA -> Product Inquiries",
    "HANA -> Account Management",
    "HANA -> Policy Questions",
    "Business One -> Technical Issues",
    "Business One -> Billing & Payment",
    "Business One -> Product Inquiries",
    "Business One -> Account Management",
    "Business One -> Policy Questions",
    "Jira -> Technical Issues",
    "Jira -> Billing & Payment",
    "Jira -> Product Inquiries",
    "Jira -> Account Management",
    "Jira -> Policy Questions",
    "Sourcetree -> Technical Issues",
    "Sourcetree -> Billing & Payment",
    "Sourcetree -> Product Inquiries",
    "Sourcetree -> Account Management",
    "Sourcetree -> Policy Questions",
    "Opsgenie -> Technical Issues",
    "Opsgenie -> Billing & Payment",
    "Opsgenie -> Product Inquiries",
    "Opsgenie -> Account Management",
    "Opsgenie -> Policy Questions",
    "Trello -> Technical Issues",
    "Trello -> Billing & Payment",
    "Trello -> Product Inquiries",
    "Trello -> Account Management",
    "Trello -> Policy Questions",
    "Illustrator -> Technical Issues",
    "Illustrator -> Billing & Payment",
    "Illustrator -> Product Inquiries",
    "Illustrator -> Account Management",
    "Illustrator -> Policy Questions",
    "Photoshop -> Technical Issues",
    "Photoshop -> Billing & Payment",
    "Photoshop -> Product Inquiries",
    "Photoshop -> Account Management",
    "Photoshop -> Policy Questions",
    "InDesign -> Technical Issues",
    "InDesign -> Billing & Payment",
    "InDesign -> Product Inquiries",
    "InDesign -> Account Management",
    "InDesign -> Policy Questions",
    "Premiere -> Technical Issues",
    "Premiere -> Billing & Payment",
    "Premiere -> Product Inquiries",
    "Premiere -> Account Management",
    "Premiere -> Policy Questions",
    "Apex -> Technical Issues",
    "Apex -> Billing & Payment",
    "Apex -> Product Inquiries",
    "Apex -> Account Management",
    "Apex -> Policy Questions",
    "Trailhead -> Technical Issues",
    "Trailhead -> Billing & Payment",
    "Trailhead -> Product Inquiries",
    "Trailhead -> Account Management",
    "Trailhead -> Policy Questions",
    "Visualforce -> Technical Issues",
    "Visualforce -> Billing & Payment",
    "Visualforce -> Product Inquiries",
    "Visualforce -> Account Management",
    "Visualforce -> Policy Questions",
    "Sales Cloud -> Technical Issues",
    "Sales Cloud  -> Billing & Payment",
    "Sales Cloud  -> Product Inquiries",
    "Sales Cloud  -> Account Management",
    "Sales Cloud  -> Policy Questions",
    "Tableau -> Technical Issues",
    "Tableau -> Billing & Payment",
    "Tableau -> Product Inquiries",
    "Tableau -> Account Management",
    "Tableau -> Policy Questions",
    "Microsoft PowerBI -> Technical Issues",
    "Microsoft PowerBI -> Billing & Payment",
    "Microsoft PowerBI -> Product Inquiries",
    "Microsoft PowerBI -> Account Management",
    "Microsoft PowerBI -> Policy Questions",
    "Datasource -> Technical Issues",
    "Datasource -> Billing & Payment",
    "Datasource -> Product Inquiries",
    "Datasource -> Account Management",
    "Datasource -> Policy Questions",
    "DataFlow -> Technical Issues",
    "DataFlow -> Billing & Payment",
    "DataFlow -> Product Inquiries",
    "DataFlow -> Account Management",
    "DataFlow -> Policy Questions",
    "Microsoft Power Apps -> Technical Issues",
    "Microsoft Power App -> Billing & Payment",
    "Microsoft Power App -> Product Inquiries",
    "Microsoft Power App -> Account Management",
    "Microsoft Power App -> Policy Questions",
    "Microsoft Power BI -> Technical Issues",
    "Microsoft Power BI -> Billing & Payment",
    "Microsoft Power BI -> Product Inquiries",
    "Microsoft Power BI -> Account Management",
    "Microsoft Power BI -> Policy Questions",
    "Microsoft Power Pages Automate -> Technical Issues",
    "Microsoft Power Pages Automate -> Billing & Payment",
    "Microsoft Power Pages Automate -> Product Inquiries",
    "Microsoft Power Pages Automate -> Account Management",
    "Microsoft Power Pages Automate -> Policy Questions",
    "Microsoft SharePoint -> Technical Issues",
    "Microsoft SharePoint -> Billing & Payment",
    "Microsoft SharePoint -> Product Inquiries",
    "Microsoft SharePoint -> Account Management",
    "Microsoft SharePoint -> Policy Questions",
    "SharePoint -> Technical Issues",
    "SharePoint -> Billing & Payment",
    "SharePoint -> Product Inquiries",
    "SharePoint -> Account Management",
    "SharePoint -> Policy Questions",
    "SharePoint List -> Technical Issues",
    "SharePoint List -> Billing & Payment",
    "SharePoint List -> Product Inquiries",
    "SharePoint List -> Account Management",
    "SharePoint List -> Policy Questions",
    "SharePoint Document Library -> Technical Issues",
    "SharePoint Document Library -> Billing & Payment",
    "SharePoint Document Library -> Product Inquiries",
    "SharePoint Document Library -> Account Management",
    "SharePoint Document Library -> Policy Questions",
    "Snowflake -> Technical Issues",
    "Snowflake -> Billing & Payment",
    "Snowflake -> Product Inquiries",
    "Snowflake -> Account Management",
    "Snowflake -> Policy Question",
    "SnowSQL -> Technical Issues",
    "SnowSQL -> Billing & Payment",
    "SnowSQL -> Product Inquiries",
    "SnowSQL -> Account Management",
    "SnowSQL -> Policy Question",
    "Microsoft Office -> Technical Issues",
    "Microsoft Office -> Billing & Payment",
    "Microsoft Office -> Product Inquiries",
    "Microsoft Office -> Account Management",
    "Microsoft Office -> Policy Questions",
    "Microsoft Word -> Technical Issues",
    "Microsoft Word -> Billing & Payment",
    "Microsoft Word -> Product Inquiries",
    "Microsoft Word -> Account Management",
    "Microsoft Word -> Policy Questions",
    "Microsoft Excel -> Technical Issues",
    "Microsoft Excel -> Billing & Payment",
    "Microsoft Excel -> Product Inquiries",
    "Microsoft Excel -> Account Management",
    "Microsoft Excel -> Policy Questions",
    "Microsoft PowerPoint -> Technical Issues",
    "Microsoft PowerPoint -> Billing & Payment",
    "Microsoft PowerPoint -> Product Inquiries",
    "Microsoft PowerPoint -> Account Management",
    "Microsoft PowerPoint -> Policy Questions",
]
ticket_field = "category"

model_name = "roberta-base"
model = RobertaForSequenceClassification.from_pretrained(
    model_name, num_labels=len(classes)
)
tokenizer = RobertaTokenizer.from_pretrained(model_name)

root_directory = os.path.dirname(__file__)

test_dir = os.path.join(root_directory, "..", "test_data")
data_paths = [
    # os.path.join(test_dir, "test_data_garvin", "data_translated.json"),
    # os.path.join(test_dir, "test_data_irild", "data_translated.json"),
    # os.path.join(test_dir, "test_data_fabian", "data_translated.json"),
    # os.path.join(test_dir, "test_data_sajjad", "data_translated.json"),
    # os.path.join(test_dir, "test_data_marco", "data_translated.json"),
    # os.path.join(test_dir, "test_data_tino", "data_translated.json"),
    os.path.join(test_dir, "test_data_with_gpt", "data_1.json"),
    # os.path.join(test_dir, "test_data_with_gpt", "data_2.json"),
    # os.path.join(test_dir, "test_data_with_gpt", "data_3.json"),
    # os.path.join(test_dir, "test_data_with_gpt", "data_4.json"),
    # os.path.join(test_dir, "test_data_with_gpt", "data_5.json"),
    # os.path.join(test_dir, "test_data_with_gpt", "test_data.json")
]

# Create datasets
custom_dataset = CustomDataset(tokenizer, data_paths, ticket_field, classes)
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
    val_confidence_scores = []

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

            # Calculate confidence scores
            softmax_scores = F.softmax(logits, dim=1)
            max_confidence_scores = torch.max(softmax_scores, dim=1)
            val_confidence_scores.extend(max_confidence_scores.values.cpu().numpy())

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

# Visualization of Confidence Scores
plt.figure(figsize=(10, 6))
plt.hist(val_confidence_scores, bins=50, alpha=0.7, color="blue")
plt.title(f"Confidence Score Distribution for {ticket_field}")
plt.xlabel("Confidence Score")
plt.ylabel("Number of Predictions")
plt.grid(True)

# Save Confidence Scores visualization as image
confidence_score_filename = f"confidence_scores_distribution_{ticket_field}.png"
plt.savefig(confidence_score_filename)
plt.close()

# Save the fine-tuned model
# if args.save_model:
model.save_pretrained("fine_tuned_roberta_model_" + ticket_field + "28k_data")
tokenizer.save_pretrained("fine_tuned_roberta_model_" + ticket_field + "28k_data")
