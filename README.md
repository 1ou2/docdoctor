# Setup python environment
```python3 -m venv openai-env
source openai-env/bin/activate
pip install -r requirements.txt
```
For openai ```openai python-dotenv tiktoken```
Data manipulation ```pandas scypy pypdf ```
Web server ```fastapi uvicorn jinja2 python-multipart```

# create local environment
edit .env file with credentials
```AZURE_OPENAI_KEY="abcdef"
AZURE_OPENAI_ENDPOINT="https://my.domain.com/"
```

# External links
https://cookbook.openai.com/examples/question_answering_using_embeddings
https://levelup.gitconnected.com/building-a-website-starter-with-fastapi-92d077092864

# sample data
embeddings_path = "https://cdn.openai.com/API/examples/data/winter_olympics_2022.csv"

# Azure deployment
On Mac, install azure CLI tools
```brew update && brew install azure-cli```

All azure configuration is stored in azure.env
Initial setup on azure :
1. create a dedicated ressource group RG-XX, ```AZ_RESOURCEGROUP="RG-XX"```
2. create a service principal, with ```azure-init-principal.sh``` script
3. create blob storage for static website 
```
chmod a+x azure-init-front.sh 
./deploy-azure.sh
```
Documentation 
- https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-static-website-how-to?tabs=azure-cli
- https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-cli

# back-end server
## RUN
From terminal ```uvicorn app.server:app --reload```
- uvicorn : ASGI 
- app.server : server.py python module located in app directory
- :app -> app = FastAPI()
- --reload : only in development mode
Server can be accessed 
http://127.0.0.1:8000