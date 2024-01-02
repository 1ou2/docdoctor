source azure.env

# prepare packages
FILES="requirements.txt app/server.py app/embeddingDB.py .deployment"
rm -rf dist
mkdir dist
cp $FILES dist
cd dist
rm -f ./src.zip 2> /dev/null && zip src.zip $FILES