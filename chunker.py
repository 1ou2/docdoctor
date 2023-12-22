import os,argparse, glob
from pypdf import PdfReader
import tiktoken
import pandas as pd

#
# Create chunks of text from an input directory
# 
#

class Chunker:

    def __init__(self,srcdir,chunkdir) -> None:
        self.srcdir = srcdir
        self.chunkdir = chunkdir
        self.supported_extensions = ["pdf","PDF"]
        self.createdirs([self.chunkdir])

    def pdf_extract(self,pdfname):
        reader = PdfReader(pdfname)
        nb_pages = len(reader.pages)
        print(f"file: {pdfname} nb pages: {nb_pages}")
        text = ""
        pages = []
        for i in range(len(reader.pages)):
            page = reader.pages[i]
            text = page.extract_text()
            pages.append(text)
        return pages

    def num_tokens_from_string(self, string: str, encoding_name: str) -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def createdirs(self, dirlist):
        for d in dirlist:
            if d and not os.path.exists(d):
                os.makedirs(d)

    def write_chunks(self, f, pages):
        # get only basename of the file (remove path)
        filename = str(os.path.basename(f))
        # change extension from pdf to txt
        textname = filename.removesuffix("pdf") + "txt"
       
        # split global text into chunks that have a smaller size
        # to create an embedding, the number of tokens is limited
        # as an heuristic, we use a page as a unitary chunk
        chk_id = 0
        for p in pages:
            tokens = self.num_tokens_from_string(p,"cl100k_base")
            #print(f"file {textname} tokens: {tokens}")
            
            if tokens < 8192:
                # format chunk filename so that each chunk as the same length
                # chk-001 ... chk-207
                size = len(str(len(pages)))
                str_chk_id = str(chk_id)
                while len(str_chk_id) < size:
                    str_chk_id = "0" + str_chk_id
                chunk_name = textname[:-4] +"-chk-" + str_chk_id + ".txt"
                with open(self.chunkdir+"/"+chunk_name, "w",encoding='utf-8') as chk_file:
                    chk_file.write(p)
                chk_id = chk_id +1
            else:
                raise Exception(f"max tokens exceeded - page too long - file: {textname} - page: {chk_id}")

    def create_chunks(self):
        # ONLY PDF is supported 
        # analyse all PDF files
        for ext in self.supported_extensions:
            files = sorted(glob.glob(self.srcdir+"/*."+ext))
            for f in files:
                # extract text from pdf
                if ext.lower() == "pdf":
                    chunks = chunker.pdf_extract(f)
                    chunker.write_chunks(f,chunks)
                else:
                    raise Exception(f"File extension not supported : {ext}")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Extract text from pdf")
    parser.add_argument("-d","--srcdir",help="Source directory where source files are stored",default="docs")
    parser.add_argument("-c","--chunkdir",help="Output directory where txt files are stored as chunks",default="chk")

    args = parser.parse_args()
    
    chunkdir = args.chunkdir
    srcdir = args.srcdir

    chunker = Chunker(srcdir,chunkdir)
    chunker.create_chunks()


