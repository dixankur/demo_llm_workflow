import os
import time
import openai
from dotenv import load_dotenv, find_dotenv

import docx
from docx.shared import Pt

# Read environment variables from .env file
load_dotenv(find_dotenv(), override=True)

# Set the Open AI key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")



# Read the source document from a .docx file
source_document_path = "data/Use Case Document - Doral ED Volume Prediction.docx"

# Load the .docx file and extract text
def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text

source_document = extract_text_from_docx(source_document_path)

# Target document where you want to apply the same formatting
target_document_path = "use_case_document.docx"
target_document = extract_text_from_docx(target_document_path)

# Prompt to instruct the model to mimic formatting
prompt = f"Mimic the formatting and structure from the following source document and apply it to the target document:\n\nSource Document:\n{source_document}\n\nTarget Document:\n{target_document}\n\nNew Document with Formatting:"

# Call the OpenAI API
response = openai.Completion.create(
    engine="davinci",
    prompt=prompt,
    max_tokens=150,
    temperature=0.7
)

# Extract the model's generated text
formatted_document = response.choices[0].text.strip()

print("Formatted Document:")
print(formatted_document)