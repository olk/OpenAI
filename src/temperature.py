from api import client

model = "gpt-3.5-turbo"
prefix = "es war einmal"
messages = [
        {
            "role": "system",
            "content": "Du bist ein Geschichtenerzähler."
        },
        {
            "role": "user",
            "content": prefix
        }
    ]
high_response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=100,
        stop=["\n"],
        temperature=2,
)
medium_response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=100,
        stop=["\n"],
        temperature=1,
)
low_response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=100,
        stop=["\n"],
        temperature=0,
)
high_content = high_response.choices[0].message.content
medium_content = medium_response.choices[0].message.content
low_content = low_response.choices[0].message.content
print(f"""
1. Hight temperature:
    {prefix}{high_content}
""")
print(f"""
2. Medium temperature:
    {prefix}{medium_content}
""")
print(f"""
3. Low temperature:
    {prefix}{low_content}
""")
