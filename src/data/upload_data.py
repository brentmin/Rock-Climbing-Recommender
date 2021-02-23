# Brian Cheng
# Eric Liu
# Brent Min

#uploads data onto mongodb

import json 
import csv
import pandas as pd

from pymongo import MongoClient
from src.functions import *

def upload_data(data_params, my_client):
    #uploads the cleaned climbs data to MondoDB
    climbs = my_client.MountainProject.climbs
    climbs_data_path = make_absolute(data_params["clean_data_folder"] + 'climbs.csv')
    with open(climbs_data_path) as f:
        climbs_df = pd.read_csv(f)
        print(climbs_df.iloc[0]['climb_type'])
        climbs_data = climbs_df.to_dict('records')
    for entry in climbs_data:
        climbs.replace_one(entry, entry, upsert=True)
