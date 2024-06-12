from api import client

model = "gpt-3.5-turbo"
messages = [
        {
            "role": "system",
            "content": "You are a smart and creative person."
        },
        {
            "role": "user",
            "content": "Hi there!"
        },
        {
            "role": "user",
            "content": "How is everything going?"
        }
    ]
reponse = client.chat.completions.create(
        model=model,
        messages=messages
)
print(messages[1]["content"])
print(messages[2]["content"])
print("========")
print(reponse.choices[0].message.content)
print("========")
print(reponse)
