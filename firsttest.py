import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),  
    api_version="2023-10-01-preview",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )
deployment_name='GPT4' #This will correspond to the custom name you chose for your deployment when you deployed a model. 
""" response = client.chat.completions.create(
    model="GPT4", # model = "deployment_name".
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
        {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
        {"role": "user", "content": "Do other Azure AI services support this too?"}
    ]
)

print(response.choices[0].message.content) """

response = client.chat.completions.create(
    model="GPT4", # model = "deployment_name".
    messages=[
        {"role": "system", "content": "Vous êtes un assistant d’un centre d’appel voulant aider les utilisateurs."},
        {"role": "user", "content": "Je n’arrive pas à imprimer"},
        {"role": "assistant", "content": "Vérifier si votre imprimante est bien configurée dans le panneau de configuration"},
        {"role": "user", "content": "Comment changer mon mot de passe ?"}
    ]
)
print(response.choices[0].message.content)