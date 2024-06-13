from api import client

model = "gpt-3.5-turbo"
messages = [
        {
            "role": "system",
            "content": "You are a smart and creative person."
        },
        {
            "role": "user",
            "content": "Wer war Hannibal?"
        }
    ]
short_reponse = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=50,
)
long_reponse = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=300,
)
print(messages[1]["content"])
print("========")
print(short_reponse.choices[0].message.content)
print("========")
print(long_reponse.choices[0].message.content)
