from api import get_embedding
from utils import cosine_similarity

categories = [
    'U.S. NEWS',
    'COMEDY',
    'PARENTING',
    'WORLD NEWS',
    'CULTURE & ARTS',
    'TECH',
    'SPORTS'
]


# function to classify a sentence
def classify_sentence(sentence, model):
    # get the embedding of the sentence
    sentence_embedding = get_embedding(sentence, model=model)
    # calculate the similarity score
    # between the sentence and each category
    similarity_scores = {}
    for category in categories:
        category_embeddings = get_embedding(category, model=model)
        similarity_scores[category] = cosine_similarity(sentence_embedding, category_embeddings)
    # return the categroy with the highest similarity score
    return max(similarity_scores, key=similarity_scores.get)


# classify a sentence
sentences = [
    "1 dead and 3 injured in El Paso, Texas, ,ail shooting",
    "Director Owen Kline Calls Funny Pages Hist 'Self-Critical' Debut",
    "15 spring break ideas for families, that whant to get away.",
    "The US is preparing to  send more troops tp tje Moiddle East.",
    "Get an inside look at Universal's new Super Nintendo World.",
    "Chicago Bulls win the NBA championship.",
    "The new iPhone 12 is now available.",
    "Scientists discover a new dinosaur species.",
    "The new Star Wars movie is now available.",
    "Amazon stock hits a new record hight."
]

model = 'text-embedding-ada-002'

for sentence in sentences:
    category = classify_sentence(sentence, model=model)
    print(f"'{sentence[:50]}..' => {category}")
    print()
