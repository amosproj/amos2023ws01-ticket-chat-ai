from torch.utils.data import Dataset
from sklearn.preprocessing import LabelEncoder
import torch
import json


class CustomDataset(Dataset):
    def __init__(self, tokenizer, data_paths, output_field, classes, max_length=512):
        self.tokenizer = tokenizer
        self.data_paths = data_paths
        self.data_set = []
        self.output_field = output_field
        self.max_length = max_length

        # Initialize label encoder with the given classes
        self.label_encoder = LabelEncoder()
        self.label_encoder.fit(classes)

        # Loading the data and encoding the labels
        self.load_json()

    def load_json(self):
        for data_path in self.data_paths:
            with open(data_path, "r") as file:
                data = json.load(file)
                for item in data:
                    if item["ticket"][self.output_field] in self.label_encoder.classes_:
                        self.data_set.append(item)
                    else:
                        print(f"Ungültiges Label: {item['ticket'][self.output_field]}")

    def __len__(self):
        return len(self.data_set)

    def __getitem__(self, idx):
        item = self.data_set[idx]

        # Check whether 'text' key is present in the item
        if "text" in item:
            text_description = "\n".join(item["text"])
        else:
            text_description = ""

        request_type = item["ticket"][self.output_field]

        # Kodieren des Labels
        request_type_encoded = self.label_encoder.transform([request_type])[0]

        # Tokenisieren des Textes
        inputs = self.tokenizer(
            text_description,
            add_special_tokens=True,
            max_length=self.max_length,
            padding="max_length",
            return_tensors="pt",
            truncation=True,
        )

        return {
            "input_ids": inputs.input_ids.flatten(),
            "attention_mask": inputs.attention_mask.flatten(),
            "labels": torch.tensor(request_type_encoded, dtype=torch.long),
        }
