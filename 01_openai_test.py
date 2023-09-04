import os
import openai
from dotenv import load_dotenv, find_dotenv

print(find_dotenv())
load_dotenv(find_dotenv(), override=True)

openai.api_key = os.getenv("OPENAI_API_KEY")
print(openai.api_key)

print(openai.Model.list())
