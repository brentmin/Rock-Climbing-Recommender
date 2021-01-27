# Brian Cheng
# Eric Liu
# Brent Min

# top_pop.py contains all the logic needed to return the most basic top 10 most popular/well received routes

import pandas as pd

from src.functions import make_absolute

def top_pop(data_params):
    
    # get the url at which raw data will be found
    clean_data_path = make_absolute(data_params["clean_data_folder"] + "climbs.csv")
    print(clean_data_path)
    
    # get the data
    df = pd.read_csv(clean_data_path)
    
    #returns a a simple TopPopular
    toppop = df[df['avg_rating'] >= 3.5].sort_values('num_ratings', ascending=False)[:10]
    
    toppop.to_csv('top_pop_results.csv')