import os
import time
import openai
import json
from dotenv import load_dotenv, find_dotenv

from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain

# Read environment variables from .env file
load_dotenv(find_dotenv(), override=True)

# Set the Open AI key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_code(prj_id):
    llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.7)

    # Create a basic template
    template = '''You are an experienced python programmer \
    and machine learning engineer.
    You are given a dataset with training data. \
    The dataset is in format {data_format}, and is present  \
    at {data_location}.

    You need to write a python code to train a RandomForest model \
    on the data. The target feature is '{target_feature}'. The primary ky for the \
    data is '{prim_key}'.

    Split the dataset into 80:20 ratio as training and test folds.
    Use scikit learn as your machine learnig library.

    Save the predictions from the model as 'final_predictions' in csv format \
    in the same folder as input dataset.

    Provide the generated code delimited by within a set of triple `.
    '''

    # Setup the basic prompt template
    prompt = PromptTemplate(
        input_variables=['data_format', 'data_location', 
                         'target_feature', 'prim_key'], 
        template=template
    )

    #print(table_details)

    # Use the prompt template to get answers
    chain = LLMChain(llm=llm, prompt=prompt)
    output = chain.run({'data_format': 'CSV',
                        'data_location': './data/P001/final_dataset.csv', 
                        'target_feature': 'priority', 
                        'prim_key': 'number'})

    print('Code generated ...')

    #print(output)
    final_code = output.split('```')[1]

    with open(f"./data/{prj_id}/random_forest.py", "w") as f:
        f.write(final_code)
