import weaviate
import os
import ast
import pandas as pd
from flask import Flask, request
from openai import OpenAI

app = Flask(__name__)

openai_api_key = os.getenv("OPENAI_API_KEY")
model = "gpt-3.5-turbo"
weaviate_class_name = "Article"

openai_client = OpenAI(api_key=openai_api_key)

weaviate_client = weaviate.Client(
        url="http://weaviate:8080",
        auth_client_secret={"X-Openai-Api-Key": openai_api_key},
        additional_headers={
            "X-Openai-Api-Key": openai_api_key,
        }
    )

article_class = {
        "class": weaviate_class_name,
        "description": "A article from the Simple English Wikipedia data set",
        "vectorizer": "text2vec-openai",
        "moduleConfig": {
            # Match how OpenAi created the embeddings for the `content` (`text`) field
            "text2vec-openai": {
                    "model": "ada",
                    "modelVersion": "002",
                    "type": "text",
                    "vectorizeClassName": False
                }
        },
        "properties": [
            {
                "name": "title",
                "description": "The title of the article",
                "dataType": ["text"],
                "moduleConfig": {"text2vec-openai": {"skip": True}}
            },
            {
                "name": "content",
                "description": "The content of the article",
                "dataType": ["text"],
            },
        ],
    }


def weaviate_import_data():
    counter = 0
    interval = 100

    csv_iterator = pd.read_csv(
            "data/data.csv",
            usecols=["id", "url", "title", "text", "content_vector"],
            # number of rows per chunk
            chunksize=100,
            # limit the number of rows to import
            nrows=100)

    weaviate_client.batch.configure(batch_size=100)

    with weaviate_client.batch as batch:
        for chunk in csv_iterator:
            for _, row in chunk.iterrows():
                properties = {"title": row.title, "content": row.text, "url": row.url}
                vector = ast.literal_eval(row.content_vector)
                batch.add_data_object(properties, class_name=weaviate_class_name, vector=vector)
                counter += 1
                if counter % interval == 0:
                    app.logger.debug(f"Imported {counter} articles...")

    app.logger.debug(f"Finished importing {counter} articles.")


def weaviate_semantic_search(query, prompt):
    nearText = {"concepts": [query]}
    properties = ["title", "content", "_additional {distance}"]
    limit = 3
    response = weaviate_client.query.get(
            class_name=weaviate_class_name,
            properties=properties,
    ).with_generate(grouped_task=prompt).with_near_text(nearText).with_limit(limit).do()
    app.logger.debug(response)
    result = response["data"]["Get"][weaviate_class_name]
    return result


weaviate_client.schema.delete_all()
weaviate_import_data()


@app.route("/ask", methods=["GET"])
def ask():
    question = request.args.get("q")
    prompt = """Extract the list of topics discussed in these articles:
        {content}
    """
    context = weaviate_semantic_search(question, prompt)
    return {"response": context}
