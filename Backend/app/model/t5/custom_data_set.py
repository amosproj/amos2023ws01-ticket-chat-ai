import json
from torch.utils.data import Dataset
import pandas as pd


class CustomDataset(Dataset):
    def __init__(self, tokenizer, data_path, prompt_path, max_length=1024):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.data_path = data_path
        self.prompt_path = prompt_path
        self.data_set = []
        self.prompt = ""

        # read prompt
        with open(self.prompt_path, "r") as prompt:
            self.prompt = prompt.read()

        # load data from CSV file
        self.load_csv()

    def __len__(self):
        return len(self.data_set)

    def __getitem__(self, idx):
        text_description = "\n".join(self.data_set[idx]["text"].split("\n"))
        target_json = self.data_set[idx]["ticket"]
        print(target_json)

        inputs = self.tokenizer.encode_plus(
            self.prompt + text_description,
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

    def load_csv(self):
        self.data_set = pd.read_csv(self.data_path).to_dict(orient="records")
