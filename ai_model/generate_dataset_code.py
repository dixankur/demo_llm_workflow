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
    You are given a set of dataset delimited by triple `, \
    it also contains information regarding its format, \
    its path along with corresponding column names.

    ```
    {table_set}
    ```

    Analyze the datasets, and then write a python program \
    to combine the data in all the datasets into one and \
    save the output dataset called 'final_dataset' in the same folder as input dataset.

    Provide the generated code delimited by within a set of triple `.
    '''

    # Setup the basic prompt template
    prompt = PromptTemplate(
        input_variables=['table_set'],
        template=template
    )


    # read the list of tables
    with open ('./datamodel/project_feature_list.json', "r") as f:
        table_data = json.loads(f.read())

    prj_id = "P001"
    table_details = ""

    for tab_details in table_data[prj_id]['tables']:
        table_details = table_details + f"Dataset name: {tab_details['name']} \n"
        table_details = table_details + f"Dataset format: {tab_details['format']} \n"
        table_details = table_details + f"Dataset path: ./data/{prj_id}/{tab_details['path']} \n"
        table_details = table_details + f"Dataset columns: "
        for col_idx, col_nm in enumerate(tab_details['columns']):
            if col_idx == 0:
                table_details = table_details + f"{col_nm[0]}"
            else:
                table_details = table_details + f", {col_nm[0]}"
        table_details = table_details + f"\n \n \n"

    #print(table_details)

    # Use the prompt template to get answers
    chain = LLMChain(llm=llm, prompt=prompt)
    output = chain.run({'table_set': table_details})

    print('Code generated ...')

    final_code = output.split('```')[1]

    with open(f"./data/{prj_id}/generate_dataset.py", "w") as f:
        f.write(final_code)

