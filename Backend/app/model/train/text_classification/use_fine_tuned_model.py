import torch
from transformers import RobertaForSequenceClassification, RobertaTokenizer

def load_model(model_path):
    model = RobertaForSequenceClassification.from_pretrained(model_path)
    tokenizer = RobertaTokenizer.from_pretrained(model_path)
    return model, tokenizer

def prepare_data(tokenizer, text, max_length=512):
    inputs = tokenizer(
        text,
        add_special_tokens=True,
        max_length=max_length,
        padding="max_length",
        return_tensors="pt",
        truncation=True,
    )
    return inputs

def predict(model, tokenizer, text, device):
    model.to(device)
    model.eval()

    inputs = prepare_data(tokenizer, text)
    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.logits

    print(logits)

    preds = torch.argmax(logits, dim=1)
    return preds

# Pfad zum gespeicherten Modell
model_path = "./fine_tuned_roberta_model_request_type"
model, tokenizer = load_model(model_path)

# Gerät festlegen (CUDA, wenn verfügbar, sonst CPU)
device = "cuda" if torch.cuda.is_available() else "cpu"

# Text für die Vorhersage
text = "Tableau dashboard is not reflecting real-time data. The connection to the database seems intact, but updates are delayed. This is critical for our daily operations."

# Vorhersage
predictions = predict(model, tokenizer, text, device)
print("Predictions:", predictions)
