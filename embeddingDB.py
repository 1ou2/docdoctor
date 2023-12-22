import pandas as pd
import glob,os,argparse
import tiktoken

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

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

# returns a list containing dicts [{file,chunkid,text,embedding,tokens}, ...]
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

    parser = argparse.ArgumentParser(description="Generate embedding database from a list of files")
    parser.add_argument("-c","--chunkdir",help="Input directory where txt files are stored as chunks",default="chk")
    args = parser.parse_args()

    chunkdir = args.chunkdir
    
    data = []
    df = pd.DataFrame()
    
    data=(create_data(chunkdir))
    df = pd.DataFrame(data)
    print(df)
    df.to_csv(chunkdir+".csv")
    df.to_json(chunkdir+".json")
