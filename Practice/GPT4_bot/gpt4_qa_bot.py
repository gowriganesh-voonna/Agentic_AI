import fitz
import os


CHUNK_SIZE =500

def chunk_text(text):
    words = text.split()
    return [" ".join(words[i:i+CHUNK_SIZE]) for i in range(0,len(words),CHUNK_SIZE)]
def extract_text_from_pdf(pdf_path):
    pages = fitz.open(pdf_path)
    full_text = "\n".join([page.get_text() for page in pages])

    return full_text
def add_document():
    pdf_path = input("Enter psth of pdf file : ").strip()

    if not os.path.exists(pdf_path):
        print(f"File Not found on location {pdf_path}")
        return
    text = extract_text_from_pdf(pdf_path)

    if not text :
        print("No content found please try another pdf file")
        return
    
    text_chunks = chunk_text(text)
    
    print(f"PDF Proccessed : {text_chunks}")

def query_document():
    return True
def delete_document():
    return True

def main():
    # 1.Add Document to FAISS Index
    #2. Query Document
    #3. Delete Document
    #4. Exit

    while True:
        print("\n Select an option :")
        print("1.Add Document to FAISS Index")
        print("2. Query Document")
        print("3. Delete Document")
        print("4. Exit")

        choice = int(input("please select an option (1/2/3/4) :"))

        if choice== 1:
            add_document()

        elif choice == 2:
            query_document()
        
        elif choice ==3:
            delete_document()

        elif choice == 4:
            print("Existing Application:")
            break


if __name__ == "__main__":
    main()