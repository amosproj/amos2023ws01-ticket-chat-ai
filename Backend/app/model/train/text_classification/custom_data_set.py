import json
from torch.utils.data import Dataset
from sklearn.preprocessing import LabelEncoder
import torch


class CustomDataset(Dataset):
    def __init__(self, tokenizer, data_paths, output_field, max_length=512):
        self.tokenizer = tokenizer
        self.data_paths = data_paths
        self.data_set = []
        self.output_field = output_field
        self.max_length = max_length

        self.label_encoder = LabelEncoder()
        self.label_encoder.fit(["Incident", "Service Request"])

        print("================================")
        print("labels", self.label_encoder.transform(["Incident", "Service Request"]))
        print("================================")

        self.load_json()
        all_labels = [data["ticket"][self.output_field] for data in self.data_set]
        self.label_encoder.fit(all_labels)

    def __len__(self):
        return len(self.data_set)

    def __getitem__(self, idx):
        text_description = "\n".join(self.data_set[idx]["text"])
        request_type = self.data_set[idx]["ticket"][self.output_field]

        request_type_encoded = self.label_encoder.transform([request_type])[0]

        inputs = self.tokenizer(
            text_description,
            add_special_tokens=True,
            max_length=self.max_length,
            padding="max_length",
            return_tensors="pt",
            truncation=True,
        )

        labels = torch.tensor(request_type_encoded, dtype=torch.long)

        return {
            "input_ids": inputs.input_ids.flatten(),
            "attention_mask": inputs.attention_mask.flatten(),
            "labels": labels,
        }

    def load_json(self):
        for data_path in self.data_paths:
            with open(data_path) as file:
                self.data_set += json.load(file)
