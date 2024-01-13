import pandas as pd
import glob,os,argparse
import tiktoken
from openai import AzureOpenAI
from dotenv import load_dotenv
import numpy as np
from pathlib import Path

#
# Embedding DB : a database storing embedding of text
#
# file, chunk id, text, embedding, tokens
#
# file : name of the source file
# chunk_id: file is split in chunks, id of chunk (string, e.g. 017)
# text : the text to be used
# embedding : embedding vector
# tokens : size in number of tokens of the text
#

# TODO : 
# - compute embedding value
# - create a EmbeddingDB class

class EmbeddingDB:
    def __init__(self,init_openai=False) -> None:
        # openai client
        self.client = None
        # directory where text chunks are located
        self.chunkdir = None
        # dataframe
        self.df = None
        # database name
        self.dbname = ""
        self.init_openai(init_openai)

    def init_openai(self,init):
        load_dotenv()
        if init:
            self.client = AzureOpenAI(
                api_key = os.getenv("AZURE_OPENAI_KEY"),  
                api_version = "2023-05-15",
                azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            )
        else:
            self.client = False

    def num_tokens_from_string(self,string: str, encoding_name: str) -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def cosine_similarity(self,a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    # returns a list containing dicts [{file,chunkid,text,embedding,tokens}, ...]
    def load(self,chunkdir):
        data = []
        files = sorted(glob.glob(chunkdir+"/*.txt"))
        for f in files:
            # remove path, and remove extension
            bname = str(os.path.basename(f))[:-4]
            (fname,chk_id) = bname.split("-chk-")
            print(f"fname {fname} chunk id {chk_id}")
            with open(f,"r",encoding="utf-8") as t:
                text = t.read()

            if len(text):
                tokens = self.num_tokens_from_string(text,"cl100k_base")
                # compute embedding for this text
                embedding = self.client.embeddings.create(input = [text], model="textembedding").data[0].embedding
                row = {"file":fname,"chunk_id":chk_id,"text":text,"embedding":embedding,"tokens":tokens}
                data.append(row)
        self.df = pd.DataFrame(data)
        return data
    
    def write(self,filename:str):
        if self.df is None:
            raise Exception("No data. Cannot write to disk.")
        if filename.endswith("csv"):
            self.df.to_csv(filename)
        elif filename.endswith("json"):
            self.df.to_json(filename)
        else:
            raise Exception(f"unknown format {filename}")
        
    def read(self,filename:str):
        self.dbname = Path(filename).stem
        
        if filename.endswith(".json"):
            self.df = pd.read_json(filename)
        elif filename.endswith(".csv"):
            self.df = pd.read_csv(filename)
        else:
            raise Exception(f"unknown format for file {filename}")
    
    # filter database and returns top similar documents
    #
    # query : text to search similarity
    # max_result : number of results returned
    #
    # returns an array : [(TEXT_ID, TEXT, SIMILARITY]
    def get_similar(self, query,max_result=10):
        # compute embedding of the query
        query_embedding = self.client.embeddings.create(input = [query], model="textembedding").data[0].embedding

        result = [
            {"id":i,"text":row["text"], "similarity":self.cosine_similarity(query_embedding,row["embedding"])}
            for i, row in self.df.iterrows()         
        ]
        # sort result by cosine similarity
        result.sort(key=lambda x:x["similarity"],reverse=True)
        # only return max_result items
        return result[:max_result]
    
    def get_text(self,id):
        return self.df.iloc[id]["text"]
    
    def _describe(self,df):
        print("HEAD\n")
        print(df.head())
        print("COLUMNS\n")
        # iterating the columns
        for col in df.columns:
            print(col)

        print(f"\nNB ROWS: {len(df)}\n")
        end = len(df)

        print(f"LAST ELEM:\n{df.loc[end-1]}\n")
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate embedding database from a list of files")
    parser.add_argument("-l","--load",help="Input directory where txt files are stored as chunks")
    parser.add_argument("-r","--read",help="read from a file")
    args = parser.parse_args()

    loaddir = args.load
    datafile = args.read
    
    edb = EmbeddingDB(True)
    
    if args.load:
        edb.load(loaddir)
        edb.write(loaddir +".json")
    elif args.read:
        edb.read(datafile)

       
        edb._describe(edb.df)
        iadf = pd.read_json("chk.json")
        edb._describe(iadf)

    
