import os
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
import openai

# Configuration
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']


# Import dataset
reviews = pd.read_csv("data/reviews.csv")

# Get embeddings
tqdm.pandas(desc="Embedding reviews")
reviews['ada_embedding'] = reviews["Review"].progress_apply(lambda x: get_embedding(x))
reviews.to_csv('output/embedded_reviews.csv', index=False)