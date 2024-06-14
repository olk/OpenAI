from api import client

model = "gpt-3.5-turbo"
messages = [
        {
            "role": "system",
            "content": "You are a smart and creative person."
        },
        {
            "role": "user",
            "content": "Who is Hannibal?"
        }
    ]
reponse_1 = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=300,
        stop=["."]
)
reponse_2 = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=300,
        stop=["\n", "user:", "assistant:"]
)
print(messages[1]["content"])
print("========")
print(reponse_1.choices[0].message.content)
print("========")
print(reponse_2.choices[0].message.content)
