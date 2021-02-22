# Brian Cheng
# Eric Liu
# Brent Min

#uploads data onto mongodb

import json 
import csv
import pandas as pd

from pymongo import MongoClient


def upload_data(data_params, my_client):
    climbs = myclient.MountainProject.climbs

    data_path = make_absolute(data_params["clean_data_folder"])

    # Turns the csv into a list of dicts, each dict is a row
    # each key in the dict is a column names
    with open(data_path) as f:
        df = pd.read_csv('/Users/brian/Desktop/Rock-Climbing-Recommender/data/cleaned/climbs.csv')
        data = df.to_dict('records')

    # Loops through and attempts to upload each row data onto mongo
    # if duplicate in mongo, replace with itself
    # if not, then insert data
    for entry in data:
        climbs.replace_one(entry, entry, upsert=True)