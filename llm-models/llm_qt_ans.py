from transformers import GPT2LMHeadModel ,GPT2Tokenizer
import torch


tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
head_model = GPT2LMHeadModel.from_pretrained("gpt2")


#by default GPT2 model is not having pad_tokens

tokenizer.pad_token = tokenizer.eos_token                # pad_token is used for adding remaining words as pad_tokens and

head_model.pad_token_id = head_model.config.eos_token_id

context = (
    "India and the United States recently agreed to remove certain tariffs that were imposed during a trade dispute. "
    "The agreement is expected to benefit key sectors such as agriculture, electronics, and manufacturing. "
    "Both governments stated that this step would strengthen economic cooperation and market access."
)


question = "What sectors will benifit from the tarrif removal"


prompt = f"\n Question : {question}   \n context : {context} "


input_ids = tokenizer.encode(prompt, return_tensors = "pt")

output_ids = head_model.generate(input_ids,max_length = 100, do_sample = True , num_return_sequences=3, temperature = 0.8)


answer_text_0 = tokenizer.decode(output_ids[0], skip_special_tokens = True)
answer_text_1 = tokenizer.decode(output_ids[1], skip_special_tokens = True)
answer_text_2 = tokenizer.decode(output_ids[2], skip_special_tokens = True)

# print  (f"\n {prompt} \n")

print  (f"\n answer_text_1 - Generated Text : {answer_text_0}")

print  (f"\n answer_text_2 - Generated Text : {answer_text_1}")

print  (f"\n answer_text_3 - Generated Text : {answer_text_2}")