# Brian Cheng
# Eric Liu
# Brent Min

# run_data.py collates all data scraping and cleaning code into one convenient place

from src.data.get_raw_data import get_raw_data
from src.functions import *

def run_data(data_params):
    """
    This function collates all scraping and cleaning code into a single function called by run.py

    TODO: move the folders from a local string to a config file?
    """
    # TODO: Delete the data folders in order to empty them, since if the user requests that data
    #       scraping code be run, then overwrite existing data

    # create the folders in which to save data if the folders do not exist
    check_folder(data_params["raw_data_folder"])
    check_folder(data_params["clean_data_folder"])

    # get raw data
    get_raw_data(data_params)

    # clean data
    # TODO
    