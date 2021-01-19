# Brian Cheng
# Eric Liu
# Brent Min

# run_data.py collates all data scraping and cleaning code into one convenient place

import requests
import json

from bs4 import BeautifulSoup
from tqdm import tqdm

from src.functions import make_absolute

def get_raw_data(data_params):
    """
    This function collates all scraping logic
    """
    # store raw data here
    raw_data = []

    # for now, just scrape Yosemite routes
    area_url = "https://www.mountainproject.com/area/105833381/yosemite-national-park"
    all_routes = find_all_routes_in_area(area_url)

    # for every route in Yosemite, get the route data
    for route_url in tqdm(all_routes):
        raw_data.append(get_route_data(route_url))

    # save the raw data
    with open(make_absolute(data_params["raw_data_folder"] + "yosemite.json"), "w") as f:
        json.dump(raw_data, f)

def get_route_data(route_url):
    """
    Get all route data for a single route

    TODO: get the users who rated and their ratings for this route

    :param:     route_url   The URL at which the route lives
    """
    # TODO: document function
    text = requests.get(route_url).text
    soup = BeautifulSoup(text, 'html.parser')
    data = json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents))
    description = soup.find('div', {'class': 'fr-view'}).contents
    data['description'] = ''.join([x for x in description if isinstance(x, str)])
    data['route_url'] = route_url
    return data

def get_user_history(user_url):
    """
    Get all routes this user has climbed

    TODO: get the ratings for each route?

    :param:     user_url    The URL of the user profile
    """
    # TODO: document function
    links = []
    text = requests.get(user_url + '/ticks').text
    soup = BeautifulSoup(text, 'html.parser')
    num_pages = int(soup.find_all('a', {"class":"no-click"})[2].contents[0].strip()[-1])
    for i in range(num_pages):
        text = requests.get(user + '/ticks?page=' + str(i + 1)).text
        soup = BeautifulSoup(text, 'html.parser')
        all_links = soup.find_all('a')
        for link in all_links:
            if len(link.find_all('strong')) > 0 and len(link) < 2:
                links.append({link.find('strong').contents[0]: link.get('href')})
    return links

def find_all_routes_in_area(area_url):
    """
    Get all the URLS of all the routes that exist in the input area

    :param:     area_url    The URL of the area to look in. It does not matter how high level of 
                            an area this URL points to, as long as it is an area of some sort
    """
    def add_links(soup):
        """
        TODO

        :param:     soup    TODO
        """
        # TODO: document function
        div = soup.find('div', {'class': 'max-height max-height-md-0 max-height-xs-400'})
        if div:
            a_hrefs = div.find_all('a')
            for link in a_hrefs:
                links.append(link.get('href'))
    # TODO: document function
    text = requests.get(area_url).text
    soup = BeautifulSoup(text, 'html.parser')
    links = []
    route_links = []
    add_links(soup)
    while len(links) > 0:
        link = links[0]
        if '/area/' in link:
            text = requests.get(link).text
            new_soup = BeautifulSoup(text, 'html.parser')
            add_links(new_soup)
        else:
            if link != '#':
                route_links.append(link)
        links.remove(link)
    return route_links
