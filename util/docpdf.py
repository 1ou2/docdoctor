import pypdf
import os,argparse, shutil,glob
from pypdf import PdfReader
import tiktoken
import pandas as pd

def extract(pdfname):
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

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def createdirs(dirlist):
    for d in dirlist:
        if d and not os.path.exists(d):
            os.makedirs(d)

def create_chunks(f, pages,outputdir,chunkdir):
    # get only basename of the file (remove path)
    filename = str(os.path.basename(f))
    # change extension from pdf to txt
    textname = filename.removesuffix("pdf") + "txt"
    with open(outputdir+"/"+textname, "w",encoding='utf-8') as t:
        t.writelines(pages)
        # split global text into chunks that have a smaller size
        # to create an embedding, the number of tokens is limited
        # as an heuristic, we use a page as a unitary chunk
        chk_id = 0
        for p in pages:
            tokens = num_tokens_from_string(p,"cl100k_base")
            #print(f"file {textname} tokens: {tokens}")
            
            if tokens < 8192:
                # format chunk filename so that each chunk as the same length
                # chk-001 ... chk-207
                size = len(str(len(pages)))
                str_chk_id = str(chk_id)
                while len(str_chk_id) < size:
                    str_chk_id = "0" + str_chk_id
                chunk_name = textname[:-4] +"-chk-" + str_chk_id + ".txt"
                with open(chunkdir+"/"+chunk_name, "w",encoding='utf-8') as chk_file:
                    chk_file.write(p)
                chk_id = chk_id +1
            else:
                raise Exception(f"max tokens exceeded - page too long - file: {textname} - page: {chk_id}")

def create_data(chunkdir):
    data = []
    files = sorted(glob.glob(chunkdir+"/*.txt"))
    for f in files:
        # remove path, and remove extension
        bname = str(os.path.basename(f))[:-4]
        (fname,chk_id) = bname.split("-chk-")
        print(f"fname {fname} chunk id {chk_id}")
        with open(f,"r",encoding="utf-8") as t:
            text = t.read()

        tokens = num_tokens_from_string(text,"cl100k_base")
            
        row = {"file":fname,"chunk_id":chk_id,"text":text,"embedding":"n/a","tokens":tokens}
        data.append(row)
    return data

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Extract text from pdf")
    parser.add_argument("-d","--srcdir",help="Source directory where pdf files are stored",default="docs")
    parser.add_argument("-o","--outputdir",help="Output directory where txt files are stored",default="txt")
    parser.add_argument("-c","--chunkdir",help="Output directory where txt files are stored as chunks",default="chk")
    args = parser.parse_args()

    outputdir = args.outputdir
    chunkdir = args.chunkdir
    createdirs([outputdir,chunkdir])
    data = []
    df = pd.DataFrame()

    # analyse all PDF files
    files = sorted(glob.glob(args.srcdir+"/*.pdf"))
    for f in files:
        # extract text from pdf
        pages = extract(f)
        create_chunks(f,pages,outputdir,chunkdir)
    
    """
    data=(create_data(chunkdir))
    df = pd.DataFrame(data)
    print(df)
    df.to_csv(chunkdir+".csv")
    df.to_json(chunkdir+".json")
    """