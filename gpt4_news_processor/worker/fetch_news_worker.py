import os
import requests
import json
import uuid
from config.settings import (
    Base_url,
    NEWS_API_KEY,
    DEFAULT_QUERY,
    QUEUE_DIR,
    LOG_DIR,
    PAGE_SIZE,
    MAX_PAGES
)

from utiles.logger import get_logger
from datetime import datetime,timezone

logger = get_logger(__name__)

def fetch_articles(query):
    all_articles = []

    for page in range(1,MAX_PAGES+1):
        params = {
            "q":query,
            "pageSize":PAGE_SIZE,
            "page":page,
            "apikey":NEWS_API_KEY
        }

        response = requests.get(Base_url,params=params)
        response.raise_for_status()
        data = response.json()
        if "articles" in data:
            all_articles.extend(data["articles"])
            logger.info(f"Fetching the page : {page} -> {response.status_code} -> {response.url}")
        else:
            logger.info (f"Page {page} : Dose not have articles ")
        
        return all_articles
    
def save_articles(article):
    article_id = str(uuid.uuid4())
    article["fetched_at"]=datetime.now(timezone.utc).isoformat()
    file_path = os.path.join(QUEUE_DIR,f"{article_id}.json")

    with open(file_path,"w",encoding="utf-8") as f:
        json.dump(article,f,indent=4)
        logger.info (f"Saved article to {file_path}")
    return True

def main():
    logger.info ("Starting fetch for api....")
    # Fetch Articles
    articles = fetch_articles(query = DEFAULT_QUERY)
    logger.info (f"Total Fetched Articles are {len(articles)}")

    # Save Articles in Folder

    for idx, article in enumerate (articles):
        if article.get("title") and article.get("url"):
            save_articles(article)


if __name__ == "__main__":
    main()