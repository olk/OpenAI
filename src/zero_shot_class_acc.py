
from api import get_embedding
from utils import cosine_similarity
import pandas as pd
from sklearn.metrics import precision_score
import json

# find all categories (unique values) in the dataset
categories = set()
with open('src/data/news.json', 'r') as file:
    for line in file:
        data = json.loads(line)
        categories.add(data['category'])

categories = list(categories)


# function to classify a sentence
def classify_sentence(sentence, model):
    # get the embedding of the sentence
    sentence_embedding = get_embedding(sentence, model=model)
    # calculate the similarity score between sentence and each category
    similarity_scores = {}
    for category in categories:
        category_embeddings = get_embedding(category, model=model)
        similarity_scores[category] = cosine_similarity(sentence_embedding, category_embeddings)
    # return the category with the highest similarity score
    return max(similarity_scores, key=similarity_scores.get)


def evaluate_precission(categories):
    # load the dataset
    df = pd.read_json('src/data/news.json', lines=True).head(20)

    y_true = []
    y_pred = []

    model = 'text-embedding-ada-002'

    # classify each sentence
    for _, row in df.iterrows():
        real_category = row['category']
        predicted_category = classify_sentence(row['headline'], model=model)

        y_true.append(real_category)
        y_pred.append(predicted_category)

        if real_category != predicted_category:
            print("[] Incorrect prediction: "
                f"{row['headline'][:50]}...\n"
                f"Real: {real_category[:20]}\n"
                f"Predicted: {predicted_category[:20]}")
        else:
            print("[] correct prediction: "
                    f"{row['headline'][:50]}...\n"
                    f"Real: {real_category[:20]}\n"
                    f"Predicted: {predicted_category[:20]}")

    return precision_score(y_true, y_pred, average='micro', labels=categories)


precision = evaluate_precission(categories)
print(f"Precision: {precision}")
