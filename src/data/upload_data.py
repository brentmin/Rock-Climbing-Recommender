# Brian Cheng
# Eric Liu
# Brent Min

#uploads data onto mongodb

import json 
import csv

from get_clean_data import split_into_user_climb

from pymongo import MongoClient


def upload_data():

    client_url = 'mongodb+srv://DSC102:coliniscool@cluster0.4gstr.mongodb.net/test'
    # Making Connection 
    my_client = MongoClient(client_url)

    collection = myclient.MountainProject.climbs

    data_path = make_absolute(data_params["clean_data_folder"])

    # Turns the csv into a list of dicts, each dict is a row
    # each key in the dict is a column names
    with open(data_path) as f:
        data = [{key: value for key, value in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]

    # Loops through and attempts to upload each row data onto mongo
    # if duplicate in mongo, replace with itself
    # if not, then insert data
    for entry in data:
        collection.replace_one(entry, entry, upsert=True)