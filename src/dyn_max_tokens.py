import sys
from api import client

model = "gpt-3.5-turbo"
# read the number of tasks form the command line
try:
    number_of_tasks = int(sys.argv[1])
except:
    print("Provide the numer of tasks")
    exit()
# create a prompt ot guid the model
prompt = """
Create a to-do list to create a company in US

Task !:
"""
stop = [
        f"Task {number_of_tasks + 1}:",
        "assistent:",
        "user:"
]
print(stop)
max_tokens = number_of_tasks * 113 + 17
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
reponse = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        stop=stop,
)
output = reponse.choices[0].message.content
print("Task 1: " + output)
