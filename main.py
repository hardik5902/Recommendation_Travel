from flask import Flask, request
import pandas as pd
import numpy as np
from contentBased import *
import random 

app = Flask(__name__)

@app.route('/placeName', methods=['POST'])
def hello():
    if request.method == 'POST':
        data = request.json
        df_places = pd.read_csv('lat3.csv')
        places = data['Place']
        output = {}
        for place in places:
            if place in df_places['Place'].unique():
                # Place id is [2251 'Mumbai' 'Marine Drive' 7500 1635 18] 
                id = df_places[df_places['class']==place].values[0]
                output[place] = recommend(id[3], num=5)
                for place_details in output[place]:
                    place_details_dict = {'lat': place_details[1], 'long': place_details[2], 'image_url': place_details[3]}
                    place_details_dict.update({'place_name': place_details[0]})
                    output[place][output[place].index(place_details)] = place_details_dict
                
        return output

@app.route('/city', methods=['POST'])
def find_places():
    if request.method == 'POST':
        data = request.json

        city = data['city']
        output = {}

        num_ratings = pd.read_csv('num_ratings.csv')
        df_places = pd.read_csv('lat3.csv')

        for CITY in city:
            try:
                my_dict = dict()
                places = list(num_ratings[num_ratings['City']==CITY]['Place'])

                for x,y in zip(places, list(num_ratings[num_ratings['City']==CITY]['Num_of_Rating'])):
                    my_dict[x] = y

                sorted_keys = sorted(my_dict, key=lambda x: my_dict[x], reverse=True)

                sorted_dict = dict([(key, my_dict[key]) for key in sorted_keys[:7]])
                places_output = []
                for place, val in sorted_dict.items():
                    lat, long = get_place_details(df_places[df_places['Place']==place].values[0][3])
                    image_url = df_places[df_places['Place']==place].values[0][-1]
                    places_output.append({'place':place, 'lat':lat, 'long':long, 'image_url':image_url})
                output[CITY] = {'output':True, 'num':len(places), 'places':places_output}
            except Exception as e:
                output[CITY] = {'output':False}
        return output

if __name__ == '__main__':
    app.run(debug=True)
