import weaviate
import os
from flask import Flask, request
from openai import OpenAI

app = Flask(__name__)

openai_api_key = os.getenv("OPENAI_API_KEY")
system_prompt = "You are a helpful assistant"
system_prompt = {"role": "system", "content": system_prompt}
model = "gpt-3.5-turbo"
weaviate_class_name = "ChatMessage"
weaviate_limit = 10
interactions_limit = 10
weaviate_certainty = 0.5

openai_client = OpenAI(api_key=openai_api_key)

weaviate_client = weaviate.Client(
        url="http://weaviate:8080",
        auth_client_secret={"X-Openai-Api-Key": openai_api_key},
        additional_headers={
            "X-Openai-Api-Key": openai_api_key,
        }
    )

schema = {
        "classes": [
            {
                "class": weaviate_class_name,
                "description": "A class to store chat messages",
                "properties": [
                    {
                        "name": "content",
                        "description": "The content of the chat message",
                        "dataType": ["text"],
                    },
                    {
                        "name": "role",
                        "description": "The role of the message",
                        "dataType": ["string"],
                    },
                ],
            }
        ]
    }


def weaviate_create_schema():
    try:
        weaviate_client.schema.create(schema)
        app.logger.info("Schema successfully created.")

    except Exception as e:
        app.logger.info(f"Failed to create schema: {e}")


def weaviate_delete_data():
    try:
        weaviate_client.schema.delete_class(class_name=weaviate_class_name)
        app.logger.info("Schema successfully reset.")

    except Exception as e:
        app.logger.info(f"Error while deleting class: {e}")
        return {"error in weaviate_reset": str(e)}, 500


weaviate_delete_data()
weaviate_create_schema()


def weaviate_nearest_interactions(query, certainty, limit):
    try:
        result = weaviate_client.query.get(
                class_name=weaviate_class_name,
                properties=["role", "content"]
            ).with_near_text({
                "concepts": [query],
                "certainty": certainty
            }).with_limit(limit).do()
        return {"data": result["data"]["Get"][weaviate_class_name]}

    except Exception as e:
        app.logger.error(f"Error while searching: {e}")


def weaviate_latest_interactions(limit):
    try:
        result = weaviate_client.query.get(
                class_name=weaviate_class_name,
                properties=["role", "content"]
            ).with_limit(limit).do()
        return {"data": result["data"]["Get"][weaviate_class_name]}

    except Exception as e:
        app.logger.error(f"Error while searching: {e}")


def weaving_save_data(data):
    weaviate_client.batch.configure(batch_size=100)
    with weaviate_client.batch as batch:
        for _, d in enumerate(data):
            properties = {"role": d["role"], "content": d["content"]}
            batch.add_data_object(properties, weaviate_class_name)


@app.route("/ask", methods=["GET"])
def ask():
    question = request.args.get("q")
    user_prompt = {
            "role": "user",
            "content": question
        }
    context = weaviate_nearest_interactions(
            question,
            weaviate_certainty,
            weaviate_limit)
    latest_interactions = weaviate_latest_interactions(interactions_limit)
    global_context = latest_interactions["data"]
    if context["data"] is not None:
        global_context = global_context + context["data"]
    global_context = [
            dict(t) for t in {tuple(d.items()) for d in global_context}
        ]
    messages = [system_prompt] + global_context + [user_prompt]
    response = openai_client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=200,
            temperature=1.2)
    content = response.choices[0].message.content.strip()
    assistant_prompt = {
            "role": "assistant",
            "content": content
        }
    data = [
            user_prompt,
            assistant_prompt
        ]
    weaving_save_data(data)
    return {
            "response": assistant_prompt["content"],
            "global_context": global_context
        }


@app.route("/data", methods=["GET"])
def weaviate_get_all_data():
    try:
        result = weaviate_client.query.get(
                class_name=weaviate_class_name,
                properties=["role", "content"]
            ).do()
        return {"data": result["data"]["Get"][weaviate_class_name]}

    except Exception as e:
        app.logger.error(f"Error while getting data: {e}")
        return {"error in weaviate_data": str(e)}, 500
