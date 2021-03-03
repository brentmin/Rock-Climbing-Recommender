# Brian Cheng
# Eric Liu
# Brent Min

# cosine_rec.py contains all the logic needed to return the routes based on your past ratings

import pandas as pd
from pymongo import MongoClient

from src.functions import make_absolute

from math import sin, cos, sqrt, atan2, radians

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import requests
from bs4 import BeautifulSoup, Tag
import json

from src.model.model_functions import filter_df, format_df, generate_notes

def cosine_rec(args=None, data_params=None, web_params=None):
    """
    TODO

    :param:     args            TODO
    :param:     data_params     TODO
    :param:     web_params      TODO
    """
    # change behavior if testing
    if((args is not None) and args["test"]):
        # get the url at which raw data will be found
        clean_data_path = make_absolute(data_params["clean_data_folder"] + "climbs.csv")
        print(clean_data_path)
        
        # get the data
        df = pd.read_csv(clean_data_path)
    else:
        # accessing the data from our MongoDB
        client = MongoClient('mongodb+srv://DSC102:coliniscool@cluster0.4gstr.mongodb.net/MountainProject?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE')
        
        # get the data
        climbs = client.MountainProject.climbs
        df = pd.DataFrame.from_records(list(climbs.find()))

    # cleans the data
    df = df.fillna(-1)
    df['climb_type'] = df['climb_type'].apply(lambda x: x.strip('][').split(', '))   

    # filter the df based on the web params
    df = filter_df(df, web_params["location"], web_params["max_distance"], 
        web_params["difficulty_range"])

    #get user's past rating data
    user = web_params['user_url']
    history = get_user_history(user)

    #routes the user has completed that are also in our DB
    user_df = pd.DataFrame(history)
    merged_df = user_df.merge(df_filtered, how='inner', on=['name', 'url'])

    #defining favorite as highest rated
    fav_routes = merged_df[merged_df['user_rating'] == merged_df['user_rating'].max()]

    #only look at the numerical attributes so far (will create more later)
    fav_routes_selected_attributes = fav_routes[['latitude', 'longitude', 'avg_rating', 'num_ratings', 'height_ft', 'height_m', 'pitches', 'grade', 'difficulty']]
    df_selected_attributes = df_filtered[['latitude', 'longitude', 'avg_rating', 'num_ratings', 'height_ft', 'height_m', 'pitches', 'grade', 'difficulty']]

    #cosine similarity function
    def find_similarity(x, current_row):
        output = pd.DataFrame(columns=['row', 'similarity_score', 'similar_to'])
        for index, row in df_selected_attributes.iterrows():
            similarity_score = round(cosine_similarity(np.array(x), [row.tolist()])[0][0], 6) #need to round because output is weird
            if similarity_score < 1: #so that you don't recommend yourself
                output.loc[len(output.index)] = [index, similarity_score, current_row]
        return output

    #find row indicies in the database where the similarity scores are highest
    output = pd.DataFrame(columns=['row', 'similarity_score', 'similar_to'])
    for index, row in fav_routes_selected_attributes.iterrows():
        output = output.append(find_similarity([row.tolist()], index), ignore_index=True)
        
    #only output the top N recommendations
    output = output.sort_values(by='similarity_score', ascending=False)[:web_params['num_recs']]
    
    #final list of recommendations with however many recommendations are requested
    final = df.iloc[output['row']][:web_params["num_recs"]]

    # generate any generic notes
    notes = generate_notes(final, web_params)
    
    # create the formatted recommendations dict based on the number of recommendations to output
    result = format_df(final)

    # put results and notes together and return 
    return  {"recommendations": result, "notes": notes}

def get_user_history(user_url):
    output = pd.DataFrame(columns=['name', 'url', 'user_rating'])
    text = requests.get(user_url + '/ticks').text
    soup = BeautifulSoup(text, 'html.parser')
    num_pages = int(soup.find_all('a', {"class":"no-click"})[-1].contents[0].strip()[-1])
    for i in range(num_pages):
        text = requests.get(user_url + '/ticks?page=' + str(i + 1)).text
        soup = BeautifulSoup(text, 'html.parser')
        all_links = soup.find_all('a')
        all_ratings = [] #this is the list of all star ratings on the current page
        for link in all_links:
            #this part is finding out the star ratings
            ratings_list = link.find_all('span', {"class":"scoreStars"})
            if len(ratings_list) > 0:
                rating = 0
                for element in ratings_list[0].contents:
                    if isinstance(element, Tag):
                        image = element['src']
                        if image == '/img/stars/starBlue.svg':
                            rating += 1
                        if image == '/img/stars/starBlueHalf.svg':
                            rating += 0.5
                all_ratings.append(rating)
            #this part is adding the data to the final output list
            if len(link.find_all('strong')) > 0 and len(link) < 2:
                #key is the name of the route, value is (route url, user's star rating for this route)
                output.loc[len(output.index)] = [link.find('strong').contents[0], link.get('href'), all_ratings.pop(0)]
    return output.to_dict()