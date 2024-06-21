import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

env_path = find_dotenv()
load_dotenv(dotenv_path=env_path, verbose=True)
client = OpenAI(api_key=os.environ["API_KEY"])


def get_embedding(text, model):
    text = text.replace('\n', ' ')
    return client.embeddings.create(
            input=[text],
            model=model).data[0].embedding
