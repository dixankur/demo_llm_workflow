import os
import openai
from dotenv import load_dotenv, find_dotenv

from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain

# Read environment variables from .env file
load_dotenv(find_dotenv(), override=True)

# Set the Open AI key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Chat GPT llm
llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.5)

# Create a basic template
template = '''You are an experienced virologist.
Write a few sentences about the following {virus} in {langauge}
'''

# Setup the basic prompt template
prompt = PromptTemplate(
    input_variables=['virus', 'langauge'],
    template=template
)

# Use the prompt template to get answers
chain = LLMChain(llm=llm, prompt=prompt)
output = chain.run({'virus': 'HIV', 'langauge': 'English'})

print(output)
