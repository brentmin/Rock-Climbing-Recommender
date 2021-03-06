# Brian Cheng
# Eric Liu
# Brent Min

# top_pop.py contains a top popular recommender, where climbs are first filtered to those over
# 3.5/4 stars, then sorted by number of reviews.

import pandas as pd
from pymongo import MongoClient

from src.functions import make_absolute
from src.model.model_functions import filter_df, format_df, generate_notes

from math import sin, cos, sqrt, atan2, radians

def top_pop(args=None, data_params=None, web_params=None):
    """
    A simple top popular which takes climbs over 3.5/4 stars and returns those climbs with the
    most number of reviews.

    :param:     args            Command line arguments
    :param:     data_params     Data params for running the project from the command line
    :param:     web_params      Params from the website

    :return:    dict            A dictionary in the following format:   
                                {
                                    "recommendations": [{"name": str, "url": int, "reason": str,
                                        "difficulty": str, "description": str}, {}, ...],
                                    "notes": str
                                }
                                Where each item in the "recommendations" list is a singular 
                                recommendation. All recommenders should return in this format
    """
    # access MongoDb
    client = MongoClient('mongodb+srv://DSC102:coliniscool@cluster0.4gstr.mongodb.net/MountainProject?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE')
    
    #set the query range
    #1 latitude ~= 69 miles
    #1 longitude ~= 54.6 miles
    latitude_min = web_params[0] - 69 * web_params['max_distance']
    latitude_max = web_params[0] + 69 * web_params['max_distance']
    longitude_min = web_params[1] - 54.6 * web_params['max_distance']
    longitude_max = web_params[1] + 54.6 * web_params['max_distance']

    # get the data
    climbs = client.MountainProject.climbs
    df = pd.DataFrame.from_records(list(climbs.find({"latitude": {"$gte": latitude_min, "$lte": latitude_max}, "longitude": {"$gte": longitude_min, "$lte": longitude_max}})))

    # cleans the data
    df['climb_type'] = df['climb_type'].apply(lambda x: x.strip('][').split(', '))

    # do a simple top popular
    toppop = df[df['avg_rating'] >= 3.5].sort_values('num_ratings', ascending=False)

    # filter based on params from the web app
    toppop = filter_df(toppop, web_params["location"], web_params["max_distance"], 
        web_params["difficulty_range"])

    # get however many recommendations are requested
    toppop = toppop[:web_params["num_recs"]]

    # generate any generic notes
    notes = generate_notes(toppop, web_params)
    
    # create the formatted recommendations dict based on the number of recommendations to output
    result = format_df(toppop)

    # put results and notes together and return 
    return  {"recommendations": result, "notes": notes}
