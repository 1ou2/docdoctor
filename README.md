# Setup python environment
```
python3 -m venv .venv
source .venv/env/bin/activate
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
chmod a+x azure-*.sh 
./azure-init-front.sh
```
Documentation 
- https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-static-website-how-to?tabs=azure-cli
- https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-cli

# back-end server
## RUN Locally
From terminal ```uvicorn app.server:app --reload```
- uvicorn : ASGI 
- app.server : server.py python module located in app directory
- :app -> app = FastAPI()
- --reload : only in development mode
Server can be accessed 
http://127.0.0.1:8000

## Azure deployment
Check logs ```az webapp log tail --name $AZ_WEBAPP_NAME --resource-group $AZ_RESOURCEGROUP ```
FastAPI deployment in a webapp is tricky because :
- Python 3.10 minimum is required
- By default, only Flask and Django are supported. The startup process launches gunicorn, and for FastAPI uvicorn is needed.

Hence, the following commands must be used :
```
az webapp config set --resource-group $AZ_RESOURCEGROUP --name $AZ_WEBAPP_NAME --linux-fx-version "PYTHON|3.12"
az webapp config appsettings set --resource-group $AZ_RESOURCEGROUP --name $AZ_WEBAPP_NAME --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true
az webapp config set --name $AZ_WEBAPP_NAME --resource-group $AZ_RESOURCEGROUP --startup-file "python -m uvicorn app.server:app --host 0.0.0.0"
```

## Secrets
Secrets are stored in Azure Keyvault.
To set a secret, go the webapp>configuration>application settings and create a new entry.
Secrets are retreivde using environment variables ```os.getenv["app_setting_name"]```

# Frontend server
# local storage
Local storage is used to store the authentication bearer
```
// Store data
var someData = 'The data that I want to store for later.';
localStorage.setItem('myDataKey', someData);

// Get data
var data = localStorage.getItem('myDataKey');

// Remove data
localStorage.removeItem('myDatakey');
```