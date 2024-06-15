from api import client

model = "gpt-3.5-turbo"
prompt_1 = """
Huawei:
company

Google:
company

Microsoft:
company

Apple:
"""
prompt_2 = """
Huawei:
company

Google:
company

Microsoft:
company

Apricot:
    fruit

Apple:
"""
for prompt in [prompt_1, prompt_2]:
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
    )
    output = response.choices[0].message.content
    print(output)
    print()
