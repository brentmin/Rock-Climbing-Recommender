# Brian Cheng
# Eric Liu
# Brent Min

#wipes out data from mongodb

import json 
import csv

from pymongo import MongoClient


def upload_data(data_params, my_client):
    climbs = myclient.MountainProject.climbs

    climbs.remove()
