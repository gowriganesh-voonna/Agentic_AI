# define one article
# define one prompt with article.
# for prompt gnerate ids and use headmodel
# get mean embeddings for article
#  use head model with mean embeddings  by using for loop .
# then sort the result

from transformers import GPT2Model,GPT2Tokenizer , GPT2LMHeadModel
import torch
import torch.nn.functional as F


# step define tokenizer,head_model,model (GPT2)
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
head_model = GPT2LMHeadModel.from_pretrained("gpt2")
embeddings_model = GPT2Model.from_pretrained("gpt2")


#
tokenizer.pad_token = tokenizer.eos_token
head_model.pad_token_id = head_model.config.eos_token_id

# define article

news_article = (
    "India and the United States have agreed to remove several trade tariffs in order to boost economic cooperation. "
    "This move is expected to benefit sectors like agriculture, electronics, and manufacturing while reducing costs "
    "for exporters on both sides. The agreement signals a stronger strategic alignment between the two nations."
)


# news prompt : question + context

news_prompt = f"Generate  news headline about traffis : \n {news_article} \n Headlines"

# genrate token ids for news_propmpt by using tokenizer encode 

model_input_ids = tokenizer.encode(news_prompt,return_tensors = "pt")


# pass the model input to headmodel for generating text

model_headlines =head_model.generate(
    model_input_ids, # Generate Text for news_headline_prompt
    max_new_tokens=50,
    num_return_sequences=10,
    do_sample=True,
    temperature=0.8
)


def get_mean_embeddings(input_text):
    input_text_tokens = tokenizer(input_text,return_tensors = "pt")

    with torch.no_grad():
        model_input = embeddings_model(**input_text_tokens)

        mean_embeddings = model_input.last_hidden_state.mean(dim=1)

    return mean_embeddings

article_headline = get_mean_embeddings(news_article)
results = []

for i,headline in enumerate(model_headlines):
    article = tokenizer.decode(headline,skip_special_tokens = True)
    headline_embedding = get_mean_embeddings(article)
    similarity = F.cosine_similarity(article_headline,headline_embedding).item()
    results.append((article.strip(),similarity))

results.sort(key = lambda x:x[1], reverse=True)

headlines = results[:4]

print("------Top 3 Headlines -------")

for headline,similarity in headlines :
    print("------------------------------------------------")
    print(f"Headlines : {headline}  - Score {similarity:.4f}")