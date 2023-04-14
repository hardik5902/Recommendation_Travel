import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from tqdm import tqdm

recommender = pd.read_csv('lat3.csv')
df = recommender.reset_index(drop=True)

# compute a TFIDF on the titles of the places
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(df['Place'])

# get cosine similarities: this takes a lot of time on the real dataset
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

# generate in 'results' the most similar cities for each place: we put a pair (score, place_id)
results = {}
for idx, row in df.iterrows():
    similar_indices = cosine_similarities[idx].argsort()[:-100:-1] 
    similar_items = [(cosine_similarities[idx][i], df['PlaceID'].loc[[i]].tolist()[0]) for i in similar_indices] 
    results[idx] = similar_items[1:]

# transform a 'Place' into its corresponding City
def item(id):  
    return df.loc[df['PlaceID'] == id]['Place'].tolist()[0].split(' - ')[0] 

# transform a 'place_id' into the index id
def get_idx(id):
    return df[df['PlaceID'] == id].index.tolist()[0]

# get latitude and longitude of a place
def get_place_details(place_id):
    lat = df.loc[df['PlaceID'] == place_id]['lat'].iloc[0]
    long = df.loc[df['PlaceID'] == place_id]['long'].iloc[0]
    image_url = df.loc[df['PlaceID'] == place_id]['ImageURL'].iloc[0]
    return lat, long, image_url

# Finally we put everything together here:
def recommend(item_id, num):
    output = []
    recs = results[get_idx(item_id)][:num]   
    for rec in recs: 
        place_id = rec[1]
        place_name = item(place_id)
        lat, long, image_url = get_place_details(place_id)
        output.append((place_name, lat, long, image_url))
    return output
# example usage

