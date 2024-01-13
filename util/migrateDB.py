import pandas as pd

def describe(df):
    print("HEAD\n")
    print(df.head())
    print("COLUMNS\n")
    # iterating the columns
    for col in df.columns:
        print(col)

    print(f"\nNB ROWS: {len(df)}\n")
    end = len(df)

    print(f"LAST ELEM: {end}\n{df.loc[end-1]}\n")

if __name__ == "__main__":
    ia_df = pd.read_json("chk.json")
    pratique_df = pd.read_json("db.json")
    #describe(ia_df)
    #describe(pratique_df)

    path = {"ia1" : "Généralité sur l’IA",
    "ia2": "Data éthique - IA éthique",
    "ia3" : "IA générative",
    "ia4" : "MLOps"}

    id = len(pratique_df)
    
    new_rows =[]
    for i, row in ia_df.iterrows():
        data = { "id":id,"text":row["text"],"tags":["IA","Intelligence Artificielle"],
                "embedding":row["embedding"],"tokens":row["tokens"],"path":"Intelligence artificielle/"+path[row["file"]]}
        new_rows.append(data)
        id = id+1
        
    newdf = pd.DataFrame(new_rows)
    describe(newdf)
    pratique_df = pd.concat([pratique_df,newdf], ignore_index=True)
    describe(pratique_df)
    pratique_df.to_json("db2.json")
    

        


