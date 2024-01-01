import argparse
from app.embeddingDB import EmbeddingDB
from util.search import Query

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate embedding database from a list of files")
    parser.add_argument("-d","--datafile",help="Read data file",required=True)
    #parser.add_argument("-a","--ask",help="Read data file",required=True)
    args = parser.parse_args()
    datafile = args.datafile
    
    #ask = input("Votre requête:")
    ask = "Qu’est ce que l’apprentissage non supervisé ?"

    edb = EmbeddingDB()
    edb.read(datafile)
    
    q = Query()
    emb = q.generate_embeddings(ask)
    res = edb.filter(emb)
    for (t,s) in res:
        print("-----")
        print(f"score : {s}")
        print(t)

