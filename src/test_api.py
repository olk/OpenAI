from api import client
from pprint import pprint

for model in sorted([x.id for x in client.models.list()]):
    print(model)
