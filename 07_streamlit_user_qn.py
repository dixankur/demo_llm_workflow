import os
import time
import streamlit as st
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

# Initialize Streamlit
st.title("Transcript Analysis")

# Load the transcript data
st.write("Loading transcript data...")
loader = PyPDFLoader("./data/first-call-SNOW-ticket-categorization.pdf")
pages = loader.load()
st.write("Transcript data loaded...")

# Split the document into chunks
st.write("Generating chunks of transcript data...")
data_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=64,
    length_function=len,
    add_start_index=True,
)
chunks = data_splitter.split_documents(pages)
st.write(f'Total number of chunks generated: {len(chunks)}')

# Initialize open ai embeddings
oi_embeddings = OpenAIEmbeddings()

# Initialize pinecone
index_name = 'transcript-index'
pinecone.init(api_key=os.getenv('PINECONE_API_KEY'), environment=os.getenv('PINECONE_ENV'))

# Check if pinecone index already exists
if index_name in pinecone.list_indexes():
    st.write(f'Index {index_name} already exists. Loading embeddings...')
    vector_store = Pinecone.from_existing_index(index_name, oi_embeddings)
    st.write('embeddings loaded...')
else:
    st.write(f'Creating index {index_name} and embeddings ...')
    pinecone.create_index(index_name, dimension=1536, metric='cosine')
    time.sleep(120)
    vector_store = Pinecone.from_documents(chunks, oi_embeddings, index_name=index_name)
    st.write('embeddings completed...')

llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.7)
retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k':7})

chain = RetrievalQA.from_chain_type(llm=llm, chain_type='stuff', retriever=retriever)

# List of questions to ask
question_list = [
    (1, 'How many Speaker attended the meeting?', 
     ('You are an experienced data scientist and experienced machine learning and artificial intelligence expert. '
      'You are provided with a transcript of a meeting where a use case is being discussed about possible use of '
      'machine learning and artificial intelligence to solve a user problem. '
      'The various participants or speakers in the transcript are in format like "Speaker n (mm:ss):" '
      'where n is the speaker number and mm is time in minutes into the meeting and ss is seconds into the meeting. '
      'Based on the different number of speakers in the transcript, calculate approximately how many speakers may have attended the meeting? '
      'You must provide us an answer with your best possible guess.'
     )),
     (2, 'How would you describe the use case in one sentence?', 
     ('You are an experienced data scientist and experienced machine learning and artificial intelligence expert. '
      'You are provided with a transcript of a meeting where a use case is being discussed about possible use of '
      'machine learning and artificial intelligence to solve a user problem. '
      'How would you describe the use case in one sentence?'
     )),
     (3, 'Describe the name of the use case in 3-5 words?', 
     ('You are an experienced data scientist and experienced machine learning and artificial intelligence expert. '
      'You are provided with a transcript of a meeting where a use case is being discussed about possible use of '
      'machine learning and artificial intelligence to solve a user problem. '
      'Describe the name of the use case in 3-5 words?'
     )),
     (4, 'What is the target feature?', 
     ('You are an experienced data scientist and experienced machine learning and artificial intelligence expert. '
      'You are provided with a transcript of a meeting where a use case is being discussed about possible use of '
      'machine learning and artificial intelligence to solve a user problem. '
      'Based on above context, please tell what is the target feature?'
     )),
     (5, 'What is the unit of analysis?', 
     ('You are an experienced data scientist and experienced machine learning and artificial intelligence expert. '
      'You are provided with a transcript of a meeting where a use case is being discussed about possible use of '
      'machine learning and artificial intelligence to solve a user problem. '
      'Based on above context, please tell What is the unit of analysis?'
     )),
     (6, 'What is the current process?', 
     ('You are an experienced data scientist and experienced machine learning and artificial intelligence expert. '
      'You are provided with a transcript of a meeting where a use case is being discussed about possible use of '
      'machine learning and artificial intelligence to solve a user problem. '
      'Based on above context, please tell what is the current process being used? '
      'Please tell about current process only, do not explain about use of machine learning and AI in future.'
     )),
     (7, 'Where is the data located?', 
     ('You are an experienced data scientist and experienced machine learning and artificial intelligence expert. '
      'You are provided with a transcript of a meeting where a use case is being discussed about possible use of '
      'machine learning and artificial intelligence to solve a user problem. '
      'Based on above context, can you provide some insights about where the data might be located and in which format?'
     )),
    (8, 'What is the desired prediction frequency?', 
     ('You are an experienced data scientist and experienced machine learning and artificial intelligence expert. '
      'You are provided with a transcript of a meeting where a use case is being discussed about possible use of '
      'machine learning and artificial intelligence to solve a user problem. '
      'Based on above context, can you tell what is the desired prediction frequency of the proposed machine learning or AI model?'
     )),
     (9, 'Did anyone mention any business constraints?', 
     ('You are an experienced data scientist and experienced machine learning and artificial intelligence expert. '
      'You are provided with a transcript of a meeting where a use case is being discussed about possible use of '
      'machine learning and artificial intelligence to solve a user problem. '
      'Based on above context, can you tell about any business constraints being discussed?'
     )),
     (10, 'How long should the prediction be retained in the data warehouse?', 
     ('You are an experienced data scientist and experienced machine learning and artificial intelligence expert. '
      'You are provided with a transcript of a meeting where a use case is being discussed about possible use of '
      'machine learning and artificial intelligence to solve a user problem. '
      'Based on above context, can you tell the proposed time for the predictions from the model to be retained?'
     )),
     (11, 'What is the success criteria?', 
     ('You are an experienced data scientist and experienced machine learning and artificial intelligence expert. '
      'You are provided with a transcript of a meeting where a use case is being discussed about possible use of '
      'machine learning and artificial intelligence to solve a user problem. '
      'Based on above context, can you tell what success criterias are being discussed for the provided problem or use case?'
     )),
     (12, 'What features should be included in the dataset?', 
     ('You are an experienced data scientist and experienced machine learning and artificial intelligence expert. '
      'You are provided with a transcript of a meeting where a use case is being discussed about possible use of '
      'machine learning and artificial intelligence to solve a user problem. '
      'Based on above context, can you tell which features are proposed to be included in the dataset for the input '
      'to the machine learning model?'
     )),
]

# Streamlit UI for questions and answers
for seq, question, prompt in question_list:
    st.write('-'*30)
    st.write(f"Question {seq}: {question}")
    st.write("  ")
    st.write(f"Prompt used: {prompt}")
    answer = chain.run(prompt)
    st.write("  ")
    st.write(f"Answer: {answer}\n")
