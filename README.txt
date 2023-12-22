# Setup python environment
```python3 -m venv openai-env
source openai-env/bin/activate
pip install -r requirements.txt
```

# create local environment
edit .env file with credentials
```AZURE_OPENAI_KEY="abcdef"
AZURE_OPENAI_ENDPOINT="https://my.domain.com/"
```

# External links
https://cookbook.openai.com/examples/question_answering_using_embeddings

# sample data
embeddings_path = "https://cdn.openai.com/API/examples/data/winter_olympics_2022.csv"
