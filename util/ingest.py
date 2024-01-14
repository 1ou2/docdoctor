import os,argparse, glob
import tiktoken
from openai import AzureOpenAI
from dotenv import load_dotenv
import pandas as pd
from pypdf import PdfReader
# Ingest documentation and create a vector database

class Ingester:
    # directory : source directory where files are located
    # 
    def __init__(self,directory="",filepath:str="") -> None:
        self.sourcedir = directory
        self.filepath = filepath
        self.currentid = 0
        
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
    
    def get_pdf_text(self,pdf_file:str):
        reader = PdfReader(pdf_file)
        #nb_pages = len(reader.pages)
        #print(f"file: {pdf_file} nb pages: {nb_pages}")
        text = ""
        pages = []
        for i in range(len(reader.pages)):
            page = reader.pages[i]
            text = text + page.extract_text()
            
        return text
    
    def add_doc(self,path:str):
        tags = path.split('/')
        tags.append("text")
        if path.lower().endswith(".txt"):
            with open(path,'r') as f:
                text = text + f.read()
        elif path.lower().endswith(".pdf"):
            text = self.get_pdf_text(path)
        else:
            raise Exception(f"unsupported file format for file {os.path.basename(path)}")
        text = path + "\r\n" + text
        tokens = self.num_tokens_from_string(text)
        nbchunks = int(tokens // 8182) +1
        chunks, chunk_size = len(text), len(text)//nbchunks
        text_list = [ text[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
        for t in text_list:
            self.add_data(t,tags,pathname=path)
    
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
                    

    def write(self,dbname):
        self.df = pd.DataFrame(self.data)
        self.df.to_json(dbname)            

    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Ingest documents")
    parser.add_argument("-d","--srcdir",help="Source directory where document files are stored",default="")
    parser.add_argument("-f","--file",help="file to ingest",default="")
    parser.add_argument("-o","--output",help="Output database file",default="")
    
    args = parser.parse_args()
    srcdir = args.srcdir
    filepath = args.file
    dbname = args.output
    print(f"ARGS : {srcdir} - {filepath} - {dbname}")
    if srcdir:
        ing = Ingester(directory=srcdir)
        ing.walk()
    elif filepath:
        ing = Ingester(filepath=filepath)
        ing.add_doc(filepath)
    else:
        raise Exception("please enter directory or file name")
    if dbname:
        ing.write(dbname)
    else:
        print(ing.data)