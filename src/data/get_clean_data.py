# Brian Cheng
# Eric Liu
# Brent Min

# get_clean_data.py collates all the logic needed to clean and save data

import json
import csv

from tqdm import tqdm

from src.functions import make_absolute

def get_clean_data(data_params):
    """
    This function collates all cleaning logic

    :param:     data_params     A dictionary containing all data parameters. The only ones used are
                                the location at which to download raw data and the location at which
                                to save clean data
    """
    # get the url at which raw data will be found
    # TODO: sync up the file names between this file and get_raw_data.py
    raw_data_path = make_absolute(data_params["raw_data_folder"] + "yosemite.json")
    print(raw_data_path)
    
    # get the data
    with open(raw_data_path, "r") as f:
        raw_data = json.load(f)

    # store all clean data as a list of lists
    # note that the first input row is the column names
    climb_data = [["climb_id", "name", "description", "image_url", "latitude", "longitude", 
        "avg_rating", "num_ratings", "url"]]
    user_data = [["user_id", "climb_id", "rating"]]

    # process the data
    for climb in raw_data:
        # get the climb/user data and add it to the list of lists
        climb_row, user_rows = split_into_user_climb(climb)
        climb_data.append(climb_row)
        for user_row in user_rows:
            user_data.append(user_row)

    # save the lists of lists as csv data in the proper location
    clean_data_path = str(make_absolute(data_params["clean_data_folder"])) + "/"
    with open(clean_data_path + "climbs.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(climb_data)
    with open(clean_data_path + "users.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(user_data)

def split_into_user_climb(climb_dict):
    """
    This function takes the json for a single climb and splits the data into a primary key climb_id
    dataset and a primary key user_id dataset

    :param:     climb_dict      The full scraped contents of one climb in dict form

    :return:    ([], [[]])      A tuple containing a list, and a list of lists. The first list   
                                contains a row of the climb.csv file, and the second list of lists
                                contains user_ids, climb_ids, and user_ratings
    """
    # all the info for the climb row
    climb_id = climb_dict["route_url"].split("/")[-2]
    try:
        image_url = climb_dict["image"]
    except KeyError:
        image_url = "N/A"
    climb_row = [climb_id, climb_dict["name"], climb_dict["description"], image_url,
        climb_dict["geo"]["latitude"], climb_dict["geo"]["longitude"], 
        climb_dict["aggregateRating"]["ratingValue"], climb_dict["aggregateRating"]["reviewCount"],
        climb_dict["route_url"]]

    # all the info for the user row
    user_rows = list(map(list, climb_dict["user_ratings"].items()))
    for user_row in user_rows:
        user_row.insert(1, climb_id)

    # return the info as a tuple
    return (climb_row, user_rows)