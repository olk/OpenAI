from api import client

for model in sorted([x.id for x in client.models.list()]):
    print(model)
