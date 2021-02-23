# Brian Cheng
# Eric Liu
# Brent Min

# top_pop.py contains all the logic needed to return the most basic top 10 most popular/well received routes

import pandas as pd
from pymongo import MongoClient

from src.functions import make_absolute

from math import sin, cos, sqrt, atan2, radians

def top_pop(args=None, data_params=None, web_params=None):
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
    df['climb_type'] = df['climb_type'].apply(lambda x: x.strip('][').split(', '))

    # returns a simple TopPopular
    toppop = df[df['avg_rating'] >= 3.5].sort_values('num_ratings', ascending=False)

    # filter by location
    
    def calc_distance(x):
        # approximate radius of earth in km
        R = 6373.0
        target_lat = radians(web_params['location'][0])
        target_lon = radians(web_params['location'][1])
        x_lat = radians(x['latitude'])
        x_lon = radians(x['longitude'])
        dlon = x_lon - target_long
        dlat = x_lat - target_lat
        a = sin(dlat / 2) ** 2 + cos(target_lat) * cos(x_lat) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c * 0.621371 #convert to miles by multiplying by 0.621371
        return distance
    toppop = toppop[toppop.apply(calc_distance, axis=1) <= web_params['max_distance']]
    
    # filter by type of climb and difficulty
    def type_and_difficulty_check(x):
        if x['boulder_climb'] == 1 and x['difficulty'] >= web_params['difficulty_range']['boulder'][0] and x['difficulty'] <= web_params['difficulty_range']['boulder'][1]:
            return True
        if x['rock_climb'] == 1 and x['difficulty'] >= web_params['difficulty_range']['route'][0] and x['difficulty'] <= web_params['difficulty_range']['route'][1]:
            return True
        return False
    toppop = toppop[toppop.apply(type_and_difficulty_check, axis=1)]
    
    # create the formatted recommendations dict based on the number of recommendations to output
    result = list(toppop[['climb_id', 'name']][:web_params['num_recs']].apply(lambda x: {"name": x[1], "url": x[0]}, axis=1))

    # make sure the correct number of climbs were returned
    notes = ""
    if(len(result) < web_params["num_recs"]):
        notes = f"Could not generate {web_params['num_recs']} recommendations based on the " \
            "selected options."

    result = {"recommendations": result, "notes": notes}

    return result