import os
import time
import openai
from dotenv import load_dotenv, find_dotenv

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

import pinecone
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings

from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# Read environment variables from .env file
load_dotenv(find_dotenv(), override=True)

# Set the Open AI key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load the transcript data
loader = PyPDFLoader("./data/first-call-SNOW-ticket-categorization.pdf")
pages = loader.load()

# Split the document into chunks
data_splitter = RecursiveCharacterTextSplitter(chunk_size=256, chunk_overlap=50)
chunks = data_splitter.split_documents(pages)

print(f'Total number of chunks generated: {len(chunks)}')

# Initialize open ai embedings
oi_embeddings = OpenAIEmbeddings()

# Initialize pinecone
index_name = 'transcript-index'
pinecone.init(api_key=os.getenv('PINECONE_API_KEY'), environment=os.getenv('PINECONE_ENV'))

# check if pinecone index already exists
if index_name in pinecone.list_indexes():
    print(f'Index {index_name} already exists. Loading embeddings...')
    vector_store = Pinecone.from_existing_index(index_name, oi_embeddings)
    print('Ok')
else:
    print(f'Creating index {index_name} and embeddings ...')
    pinecone.create_index(index_name, dimension=1536, metric='cosine')
    time.sleep(120)
    vector_store = Pinecone.from_documents(chunks, oi_embeddings, index_name=index_name)
    print('Ok')

llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.7)
retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k':3})

chain = RetrievalQA.from_chain_type(llm=llm, chain_type='stuff', retriever=retriever)

question = "what is this document about?"
answer = chain.run(question)
print('-'*30)
print(f"Question: {question}")
print(f"Answer: {answer}")

question = "This is a transcript of a meeting. How many people attended the meeting?"
answer = chain.run(question)
print('-'*30)
print(f"Question: {question}")
print(f"Answer: {answer}")


