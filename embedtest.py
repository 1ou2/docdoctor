# imports
import ast  # for converting embeddings saved as strings back to arrays
from openai import AzureOpenAI # for calling the OpenAI API
import pandas as pd  # for storing text and embeddings data
import tiktoken  # for counting tokens
import os # for getting API token from env variable OPENAI_API_KEY
from scipy import spatial  # for calculating vector similarities for search
from dotenv import load_dotenv

def query():
    # models
    EMBEDDING_MODEL = "text-embedding-ada-002"
    GPT_MODEL = "gpt-3.5-turbo"

    load_dotenv()
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_KEY"),  
        api_version="2023-10-01-preview",
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        )
    deployment_name='GPT4'
    deployment_name="gpt35turbo"

    # an example question about the 2022 Olympics
    query = 'Which athletes won the gold medal in curling at the 2022 Winter Olympics?'

    response = client.chat.completions.create(
        model = deployment_name,
        messages=[
            {"role": "system", "content": "You answer questions about the 2022 Winter Olympics."},        
            {"role": "user", "content": query}
        ]
    )
    #print(response.model_dump_json(indent=2))
    print(response.choices[0].message.content)

def pddata():
    embeddings_path = "winter_olympics_2022.csv"
    df = pd.read_csv(embeddings_path)
    #print(df)
    #for i in range(10):
    #    print(df.iloc[i].loc["embedding"])
    print("########")
    print(df.iloc[3].loc["embedding"])
    print("########")
    # convert embeddings from CSV str type back to list type
    df['embedding'] = df['embedding'].apply(ast.literal_eval)
    print("--------")
    print(df.iloc[3].loc["embedding"])
    print("--------")
if __name__ == "__main__":
    pddata()