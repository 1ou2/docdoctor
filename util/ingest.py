import os,argparse, glob
import tiktoken
from openai import AzureOpenAI
from dotenv import load_dotenv
import pandas as pd
# Ingest documentation and create a vector database

class Ingester:
    # directory : source directory where files are located
    # dbname = database name
    def __init__(self,directory,dbname="db.json") -> None:
        self.sourcedir = directory
        self.currentid = 0
        # name of the database file
        self.dbname = dbname
        self.logs = {"txt":[],"pdf":[],"other":[]}
        self.data = []
        # openai handler
        self.openai = False
        self.init_openai(True)
        # dataframe object
        self.df = None

    def init_openai(self,init):
        load_dotenv()
        if init:
            self.openai = AzureOpenAI(
                api_key = os.getenv("AZURE_OPENAI_KEY"),  
                api_version = "2023-05-15",
                azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            )
        else:
            self.openai = False

    def add_data(self, text:str, tags:list,pathname:str):
        # compute embedding for this text
        embedding = self.openai.embeddings.create(input = [text], model="textembedding").data[0].embedding
        tokens = self.num_tokens_from_string(text)
       
        row = {"id": self.currentid,"text":text,"tags":tags,"embedding": embedding,"tokens":tokens,"path":pathname}
        self.currentid = self.currentid +1
        self.data.append(row)

    def num_tokens_from_string(self, string: str, encoding_name:str="cl100k_base") -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens
    
    def add_doc(self,path:str):
        if path.lower().endswith(".txt"):
            with open(path,'r') as f:
                text = path + "\r\n"
                text = text + f.read()
        tokens = self.num_tokens_from_string(text)
        if tokens < 8192:
            tags = path.split('/')
            tags.append("text")
            self.add_data(text,tags,pathname=path)
        else:
            nbchunks = int(tokens / 8182) + 1
            raise Exception(f"Token exception text too long, nb tokens = {tokens}")


    
    def load_doc(self,path:str,tags:dict):
        pass

    def walk(self):
        for root, dirs, files in os.walk(self.sourcedir):
            for f in files:
                fullpath = os.path.join(root,f)
                if f.lower().endswith(".txt"):
                    self.logs["txt"].append(fullpath)
                    self.add_doc(fullpath)
                elif f.lower().endswith(".pdf"):
                    self.logs["pdf"].append(fullpath)
                else:
                    self.logs["other"].append(fullpath)
                    

    def write(self):
        self.df = pd.DataFrame(self.data)
        self.df.to_json(self.dbname)            

    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Ingest documents")
    parser.add_argument("-d","--srcdir",help="Source directory where document files are stored",default="docs")
    parser.add_argument("-o","--output",help="Output database file",default="db.json")
    
    args = parser.parse_args()
    srcdir = args.srcdir
    dbname = args.output
    ing = Ingester(srcdir,dbname)
    ing.walk()
    
    ing.write()