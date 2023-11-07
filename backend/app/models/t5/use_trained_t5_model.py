from transformers import T5ForConditionalGeneration, T5Tokenizer

# Load the fine-tuned model and tokenizer
model = T5ForConditionalGeneration.from_pretrained("fine_tuned_t5_model")
tokenizer = T5Tokenizer.from_pretrained("fine_tuned_t5_model")

#  input text
input_text = "Translate this into Json: Hey, I'm David. I've encountered an issue with my company laptop's audio. There's no sound, and I've tried adjusting the volume settings, but it hasn't helped. It's affecting my ability to participate in virtual meetings. Can you please assist me in resolving this audio problem?"

# Tokenize and convert to tensor
input_ids = tokenizer.encode(input_text, return_tensors="pt")

# Generate response
output = model.generate(input_ids, max_length=1000, num_return_sequences=1, no_repeat_ngram_size=2, top_k=50, top_p=0.95, temperature=0.7)

# Decode and print the response
response = tokenizer.decode(output[0], skip_special_tokens=True)
print("Generated response:", response)