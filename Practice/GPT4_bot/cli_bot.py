import fitz   # pip install PyMuPDF  . fitz is original name.
import os
import openai
import sys
import faiss
import numpy as np
from dotenv import load_dotenv
import logging

# step 1
load_dotenv() # - load the enviroment variables
# openai.api_key = os.getenv("OPENAI_API_KEY")

PDF_FILE_PATH =r"D:\Practice\Agentic_AI\Practice\GPT4_bot\Microsoft Corporation Overview.pdf"

# Step 2 - Setup logging
logging.basicConfig(
    filename="cli_bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# step 3 - Read PDF File

def extract_text(pdf_file_path):
    try:
        pdf_pages=fitz.open(pdf_file_path)
        full_pdf_text ="\n".join([page.get_text() for page in pdf_pages] )
        logger.info(f"Extracted text from PDF File {pdf_file_path} with  length:{len(full_pdf_text)}")
        return full_pdf_text
    except Exception as e:
        logger.exception(f"Failed to read text from {pdf_file_path}.Error {e}")


def main():
    
    if len(sys.argv)<2:
        print(f"Tool Usage : Python gpt4-cli-bot.py {pdf_file_path} :")
        sys.exit(1)

    pdf_file_path = sys.argv[1]
    print(f"File Path : {pdf_file_path}")
    # Check if source pdf file exists
    if not os.path.exists(pdf_file_path):
        print("Source PDF File is not avaible")
        sys.exit(1)
    pdf_text = extract_text(pdf_file_path)
    print(f"\n PDF Content are : {pdf_text}")

if __name__== "__main__":
    main()

# cmd : python cli_bot.py Rahul_Krish
# use cmd: python cli_bot.py .pdf_HERE without quotes