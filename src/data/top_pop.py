# Brian Cheng
# Eric Liu
# Brent Min

# top_pop.py contains all the logic needed to return the most basic top 10 most popular/well received routes

import pandas as pd
from pymongo import MongoClient

from src.functions import make_absolute

def top_pop():
    
    '''# get the url at which raw data will be found
    clean_data_path = make_absolute(data_params["clean_data_folder"] + "climbs.csv")
    print(clean_data_path)
    
    # get the data
    df = pd.read_csv(clean_data_path)'''
    
    # accessing the data from our MongoDB
    client = MongoClient('mongodb+srv://DSC102:coliniscool@cluster0.4gstr.mongodb.net/MountainProject?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE')
    
    # get the data
    climbs = client.MountainProject.climbs
    df = pd.DataFrame.from_records(list(climbs.find()))
    
    #returns a a simple TopPopular
    toppop = df[df['avg_rating'] >= 3.5].sort_values('num_ratings', ascending=False)[:10]
    
    result_json = toppop[['climb_id', 'name']].set_index('climb_id').to_json()
    print(result_json)
    
    return 'The top 10 popular routes:' + str(result_json)