import os
import pandas as pd
import numpy as np
from api import get_embedding
from utils import (
        cosine_similarity,
        download_nltk_data,
        preprocess_text)

# download necessary NLTK data
download_nltk_data()

dataset_file_path = os.path.join(
        os.path.dirname(__file__),
        'data',
        'simplified_coffee.csv')

# read user input
input_coffee_name = input('Enter a coffee name: ')

# load CSV file into Pdatas DataFrame (only first 50 rows)
df = pd.read_csv(dataset_file_path, nrows=50)

# preprocess the review text
df['preprocessed_review'] = df['review'].apply(preprocess_text)

# the model to use
model = 'text-embedding-ada-002'
# get the embeddings from each review
review_embeddings = []
for review in df['preprocessed_review']:
    review_embeddings.append(get_embedding(review, model=model))

# get the index of the input coffee name
try:
    input_coffee_index = df[df['name'] == input_coffee_name].index[0]
except:
    print('Please eneter a valid coffee name.')
    exit()

# calculate the cosine similarity between the input coffee's review and all other reviews
similarities = []
input_review_embedding = review_embeddings[input_coffee_index]

for review_embedding in review_embeddings:
    similarity = cosine_similarity(input_review_embedding, review_embedding)
    similarities.append(similarity)

# get the indices of the most similar reviews
# (exclude the input coffee's review itself)
most_similar_indices = np.argsort(similarities)[-6:-1]

# get the names of the most similar coffees
similar_coffee_names = df.iloc[most_similar_indices]['name'].tolist()

# print the result
print('The most similar coffess to'
    f'{input_coffee_name} are:')
for coffee_name in similar_coffee_names:
    print(coffee_name)
