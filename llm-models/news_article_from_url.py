import logging
import requests
import torch
import torch.nn.functional as F
from transformers import GPT2Model,GPT2Tokenizer , GPT2LMHeadModel


NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
API_KEY = "259d402894094797b40607ced1ecbac5"
HEADLINE_COUNT =3
ARTICLE_COUNT =5

logging.basicConfig(
    level= logging.INFO,
    format = "%(asctime)s - %(levelname)s -%(message)s"
)


#define tokenizer,models
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2Model.from_pretrained("gpt2")
head_model = GPT2LMHeadModel.from_pretrained("gpt2")

tokenizer.pad_token = tokenizer.eos_token
head_model.pad_token_id = head_model.config.eos_token_id

#define model for mean embeddings
def get_mean_embeddings(input_text):
    input_text_tokens = tokenizer(input_text,return_tensors = "pt")

    with torch.no_grad():
        mean_embeddings = model(**input_text_tokens).last_hidden_state.mean(dim =1)


    return mean_embeddings


def fetch_news_article(api_key,count) -> list[dict]:
    logging.info("Fetching new articles -------Please wait")
    news_api_response = requests.get(NEWS_API_URL,
                                     params= {
                                         "apikey" : api_key,
                                         "country" :"us",
                                         "pagesize" : count
                                     })
    
    news_api_response.raise_for_status()

    news_articles = news_api_response.json().get("articles",[])
    logging.info (f"Fetched {len(news_articles)} articles")
    return news_articles

def generate_headlines(prompt):
    news_headline_tokens = tokenizer(prompt, return_tensors="pt").input_ids
    headlines = head_model.generate (
        news_headline_tokens,
        num_return_sequences = 1, # Fix the issue for Greedy - Beam message
        max_new_tokens =50,
        temperature = 0.8,
        top_k=50,
        top_p  = 0.95
    )
    return [tokenizer.decode(headline, skip_special_tokens = True).replace(prompt, "").strip() for headline in headlines]
def process_news_articles(news_articles):
    for id,news_article in enumerate(news_articles):
        content = news_article.get("content") or ""
        title = news_article.get("title")  or ""
        description = news_article.get("description") or ""
        news_text = f"{title}. {description}. {content}".strip()

        if not news_text:
            continue

        prompt =  f" Generated a headline for this news: \n {news_text}"
        headline_candidates = generate_headlines(prompt) # For a Article

        # Get the Original Prompt Embeddings
        news_text_embedding = get_mean_embeddings(prompt)

        result = []
        for headline in headline_candidates:
            headline_mean_embedding =  get_mean_embeddings(headline)
            score = F.cosine_similarity(headline_mean_embedding,news_text_embedding).item()
            result.append((headline, score)
            )

        best_headline, score = max(result, key= lambda x: x[1])
        print (f"{best_headline} - Score {score:.4f}")

        ## Todo : Write to the JSON File with 
        ## Article :
        ##      Article
        ##          News_Text
        ##          Headline
        ##              Score


if __name__ == "__main__":
    try:
        articles = fetch_news_article(API_KEY,ARTICLE_COUNT)
        #print(articles)
        process_news_articles (articles)

    except Exception as e:
        logging.info(str(e))

