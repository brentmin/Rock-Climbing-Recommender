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
    state_names = ["Arizona", "Utah"]
    # ,"Alaska", "Arkansas", "Arizona", "California", 
    #                "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", 
    #                "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", 
    #                "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", 
    #                "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", 
    #                "North Carolina", "North Dakota", "Nebraska", "New Hampshire", 
    #                "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", 
    #                "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", 
    #                "South Carolina", "South Dakota", "Tennessee", "Texas", 
    #                "Utah", "Virginia", "Vermont", "Washington", "Wisconsin", 
    #                "West Virginia", "Wyoming"]
    state_names.sort()
    for state in state_names:
        climbs = my_client.MountainProject.climbs
        climbs_data_path = make_absolute(data_params["clean_data_folder"] + state + '_climbs.csv')
        with open(climbs_data_path, encoding="utf-8") as f:
            climbs_df = pd.read_csv(f, encoding="utf-8")
            climbs_data = climbs_df.to_dict('records')
        for entry in climbs_data:
            climbs.replace_one(entry, entry, upsert=True)
