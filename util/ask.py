import argparse
from embeddingDB import EmbeddingDB
from search import Query

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate embedding database from a list of files")
    parser.add_argument("-d","--datafile",help="Read data file",required=True)
    #parser.add_argument("-a","--ask",help="Read data file",required=True)
    args = parser.parse_args()
    datafile = args.datafile
    
    #ask = input("Votre requête:")
    ask = "quels est la politique salariale d’orange"

    edb = EmbeddingDB()
    edb.read(datafile)
    

    res = edb.get_similar(ask,max_result=3)
    context = ""
    for r in res:
        print(f"score: {r['similarity']}")
        if float(r['similarity']) > 0.8:
            context = context + r['text']
    q = Query()
    response = q.answer(ask,context)
    print(response)
    for r in res:
        print(f"score: {r['similarity']}")
    

    
        

