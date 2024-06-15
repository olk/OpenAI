from api import client

model = "gpt-3.5-turbo"
prompt = """
    Write a concise paragraph about the lyrical
    characteristics and themes of old-school rap.
"""
messages = [
        {
            "role": "system",
            "content": "You are a smart assistant."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=200,
        temperature=0.5,
        stop=["assistanti:", "user:"]
)
output = response.choices[0].message.content
prompt = f"""Context: {output}
Task: Create lyrics for an old-school rap song about justice and lone wolf.
"""
messages = [
        {
            "role": "system",
            "content": "You are a popular old-school rap lyricist."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=500,
        temperature=1,
        stop=["assistanti:", "user:"]
)
output = response.choices[0].message.content
print(f"The prompt fed to the model\n\n{prompt}")
print()
print(f"The result: \n\n{output}")
