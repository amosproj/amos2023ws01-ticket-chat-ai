import json
from torch.utils.data import Dataset


class CustomDataset(Dataset):
    def __init__(
        self, tokenizer, data_paths, output_field, max_length=1024
    ):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.data_paths = data_paths
        self.data_set = []
        self.output_field = output_field

        # load data from files
        self.load_json()

    def __len__(self):
        return len(self.data_set)

    def __getitem__(self, idx):
        text_description = "\n".join(self.data_set[idx]["text"])
        request_type = self.data_set[idx]["ticket"][self.output_field]

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
            "labels": request_type,
        }

    def load_json(self):
        for data_path in self.data_paths:
            with open(data_path) as file:
                self.data_set += json.load(file)
