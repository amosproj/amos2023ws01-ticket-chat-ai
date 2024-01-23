from transformers import T5ForConditionalGeneration, T5Tokenizer

# Initialize the T5 tokenizer and model
model_name = "text_generation_t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Input text
input_text = "Translate this into Json: Hey, I'm David. I've encountered an issue with my company laptop's audio. There's no sound, and I've tried adjusting the volume settings, but it hasn't helped. It's affecting my ability to participate in virtual meetings. Can you please assist me in resolving this audio problem?"

# Tokenize the input text
input_ids = tokenizer.encode(
    input_text, return_tensors="pt", max_length=512, truncation=True
)

# Generate text
output = model.generate(input_ids)

# Decode and print the generated text
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print("Generated text:", generated_text)
