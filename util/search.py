# imports
import ast
import argparse
from math import cos  # for converting embeddings saved as strings back to arrays
from openai import AzureOpenAI # for calling the OpenAI API
import pandas as pd  # for storing text and embeddings data
import tiktoken  # for counting tokens
import os # for getting API token from env variable OPENAI_API_KEY
from scipy import spatial  # for calculating vector similarities for search
from dotenv import load_dotenv
import numpy as np

class Query:
    def __init__(self) -> None:
        self.deployment_name="gpt35turbo"
        self.init_openai()

    def init_openai(self):
        load_dotenv()
        self.client = AzureOpenAI(
            api_key = os.getenv("AZURE_OPENAI_KEY"),  
            api_version = "2023-05-15",
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        )

    def num_tokens_from_string(self,string: str, encoding_name: str) -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def generate_embeddings(self, text, model="textembedding"):
        return self.client.embeddings.create(input = [text], model=model).data[0].embedding

    def cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    def answer(self, query, context):
        context_query = f"""
<CONTEXTE>
{context}
</CONTEXTE>

<REQUETE>
{query}
</REQUETE>
"""
        print(context_query)

        systemprompt = """Vous êtes un assistant de support informatique. 
        En utilisant les données fournies en contexte, répondez en français à la requête de l’utilisateur. 
        Si vous avez besoin d’informations complémentaires demandez-les.
"""
        response = self.client.chat.completions.create(
        model = self.deployment_name,
        messages=[
            {"role": "system", "content": systemprompt},        
            {"role": "user", "content": context_query}
        ]
        )
        return response.choices[0].message.content


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate embedding database from a list of files")
    parser.add_argument("-q","--query",help="query")
    args = parser.parse_args()
