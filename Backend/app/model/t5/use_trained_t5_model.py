import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

from app.enum.customer_prio import CustomerPrio
from app.enum.prio import Prio


class TrainedT5Model:
    def __init__(self, model: T5ForConditionalGeneration, tokenizer: T5Tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def run_model(self, text):
        # Load the fine-tuned model and tokenizer
        model = self.model
        tokenizer = self.tokenizer

        #  input text
        # input_text = "Translate this into Json: Hey, I'm David. I've encountered an issue with my company laptop's audio. There's no sound, and I've tried adjusting the volume settings, but it hasn't helped. It's affecting my ability to participate in virtual meetings. Can you please assist me in resolving this audio problem?"
        input_text = "Translate this into Json: " + text

        # Tokenize and convert to tensor
        input_ids = tokenizer.encode(input_text, return_tensors="pt")

        # Generate response
        output = model.generate(
            torch.Tensor(input_ids),
            max_length=1000,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
        )

        # Decode and print the response
        response = tokenizer.decode(output[0], skip_special_tokens=True)

        return self.convert_output_to_dict(response)

    def convert_output_to_dict(self, text):
        # dictionary representing ticket structure
        response = {
            "title": "",
            "service": "",
            "category": "",
            "keywords": [],
            "customerPriority": CustomerPrio.can_work,
            "affectedPerson": "",
            "description": "",
            "priority": Prio.low,
            "attachments": [],
        }

        response["title"] = self.extract_value(text, "title")
        response["service"] = self.extract_value(text, "service")
        response["category"] = self.extract_value(text, "category")
        response["keywords"] = self.extract_value(text, "keywords")
        response["affectedPerson"] = self.extract_value(text, "affectedPerson")
        response["description"] = self.extract_value(text, "description")

        prio = self.extract_value(text, "priority")

        if prio == "Medium":
            response["priority"] = Prio.medium
        elif prio == "High":
            response["priority"] = Prio.high
        elif prio == "Low":
            response["priority"] = Prio.low

        return response

    def extract_value(self, text, key):
        # Replace incorrect characters in the text
        text = (
            text.replace("«", '"')
            .replace("»", '"')
            .replace("„", '"')
            .replace("“", '"')
            .replace("”", '"')
            .replace("=", " ")
            .replace("-", " ")
            .replace("—", " ")
            .replace(":", " ")
            .replace(";", " ")
        )

        # Split the text into a list using double quotation marks as the delimiter
        result_list = text.split('"')

        # Remove empty strings from the list
        result_list = [item for item in result_list if item.strip()]

        result = self.get_value_after_key(result_list, key)

        return result

    def get_value_after_key(self, text_list, key):
        # Find the index of the key in the list
        key_index = None
        for word in text_list:
            if key in word:
                key_index = text_list.index(word)

        # If the key is found and there is a next string, return it
        if key_index is not None and key_index + 1 < len(text_list):
            return text_list[key_index + 1]
        else:
            if key == "keywords":
                return []
            return ""
