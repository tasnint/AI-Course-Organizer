import os
import shutil
import datetime
import schedule
import time
import json
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from docx import Document
import nltk
nltk.download('punkt')
import openai

from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import VectorDBQA
# If CharacterTextSplitter is part of a specific module in the updated library
from langchain.text_splitter import CharacterTextSplitter


# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_SECRET_KEY")

source_dir = "/mnt/c/Users/tanis/Downloads"

def load_courses(filename='courses.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_courses(courses, filename='courses.json'):
    with open(filename, 'w') as file:
        json.dump(courses, file)

def ask_user_to_add_course():
    print("Would you like to add a course?")
    response = input("If yes, type 'Y': ")
    if response.lower() == 'y':
        course_code = input("Enter course code here: ")
        course_description = input("Enter course description here: ")
        return (course_code, course_description)
    return None

def read_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ''.join([page.extract_text() or "" for page in reader.pages])
        return text
    except Exception as e:
        print(f"Error reading PDF file {file_path}: {e}")
        return ""

def read_docx(file_path):
    try:
        doc = Document(file_path)
        return "\n".join(paragraph.text for paragraph in doc.paragraphs if paragraph.text)
    except Exception as e:
        print(f"Error reading DOCX file {file_path}: {e}")
        return ""

def read_txt(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except Exception as e:
        print(f"Error reading TXT file {file_path}: {e}")
        return ""

class DocumentContent:
    def __init__(self, content, metadata={}):
        self.page_content = content
        self.metadata = metadata  # Add metadata attribute
    
embeddings = OpenAIEmbeddings(api_key=api_key)

def categorize_documents(text, courses, retries=5):
    text_splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=0)
    texts = text_splitter.split_text(text)
    attempt = 0
    while attempt < retries:
        try:
            doc_search = Chroma.from_texts(texts, embeddings)
            chain = VectorDBQA.from_chain_type(llm=OpenAI(api_key=api_key), chain_type="stuff", vectorstore=doc_search)
            course_options = ", ".join([code for code, desc in courses])
            query = f"What course out of these: {course_options}, is this document relevant to?"
            response = chain.run(query)
            return response
        except Exception as e:
            wait_time = 2 ** attempt
            print(f"Rate limit exceeded, retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            attempt += 1
    print("Failed to categorize document after several attempts due to rate limiting.")
    return "Unknown"

def process_documents(source, courses):
    for file in os.listdir(source):
        file_path = os.path.join(source, file)
        file_extension = file.split('.')[-1]

        # First check if filename contains any course code
        for course_code, _ in courses:
            if course_code.lower() in file.lower():
                destination = os.path.join("/mnt/c/Users/tanis/Desktop", course_code)
                os.makedirs(destination, exist_ok=True)
                shutil.copy2(file_path, destination)
                print(f"Directly copied {file} to {destination} due to filename match.")
                break
        else:
            # If no course code is found in the filename, proceed with AI processing
            if file_extension in ['pdf', 'docx', 'txt']:
                text = globals()[f'read_{file_extension}'](file_path)
                response = categorize_documents(text, courses)
                print(f"Processing {file}: {response}")

                if response != "Unknown":
                    for course_code, _ in courses:
                        if course_code in response:
                            destination = os.path.join("/mnt/c/Users/tanis/Desktop", course_code)
                            os.makedirs(destination, exist_ok=True)
                            shutil.copy2(file_path, destination)
                            print(f"AI identifies {file} as relevant to {course_code} and copied it to {destination}.")
                            break


def main():
    courses = load_courses()
    new_course = ask_user_to_add_course()
    if new_course:
        courses.append(new_course)
        save_courses(courses)
    
    print("Monitoring for documents related to courses:", [(code, desc) for code, desc in courses])
    schedule.every(10).minutes.do(lambda: process_documents(source_dir, courses))
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
