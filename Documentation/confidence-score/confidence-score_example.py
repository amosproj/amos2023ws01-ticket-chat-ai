# the following code doesn't do what it is supposed to do. The confidence score couldn't be calculated for the t5 model.
# the code is written and committed as an example of what was tried and maybe a step closer on creating working code.

import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer, pipeline

model = T5ForConditionalGeneration.from_pretrained('t5-base')
tokenizer = T5Tokenizer.from_pretrained('t5-base')

# input text
input_text = ("Find the solution: Hey, I'm David. I've encountered an issue with my company laptop's audio. "
              "There's no sound, and I've tried adjusting the volume settings, but it hasn't helped. It's affecting "
              "my ability to participate in virtual meetings. Can you please assist me in resolving this audio "
              "problem?")

# Tokenize and convert to tensor
input_ids = tokenizer(text=input_text, return_tensors="pt").input_ids

# Generate response
output = model.generate(
    torch.Tensor(input_ids),
    max_length=1000,
    num_return_sequences=1,
    no_repeat_ngram_size=2,
    top_k=50,
    top_p=0.95,
    temperature=0.7,
    output_scores=True,
    return_dict_in_generate=True
)

response = tokenizer.decode(output[0][0], skip_special_tokens=True)

print(output[1])
print("RESPONSE: ", response)

# only use id's that were generated
# gen_sequences has shape [3, 15]
gen_sequences = output.sequences[:, input_ids.shape[1]:]

# let's stack the logits generated at each step to a tensor and transform
# logits to probs
probs = torch.stack(output.scores, dim=1).softmax(-1)  # -> shape [3, 15, vocab_size]

# now we need to collect the probability of the generated token
# we need to add a dummy dim in the end to make gather work
gen_probs = torch.gather(probs, 2, gen_sequences[:, :, None]).squeeze(-1)
print("SEQ: ", gen_sequences)
print("PROBS: ", gen_probs)

# pipe = pipeline("text-generation", model="t5-base")
# print(pipe(input_text))
