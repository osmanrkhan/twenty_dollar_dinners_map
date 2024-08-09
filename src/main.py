import requests
from bs4 import BeautifulSoup
import pandas as pd
import folium
from append_restaurant_list import main as update_list
from map_html_maker import drawer as update_map

def main():
    #scrapes, grabs new list, asks for some help to populate
    update_list()
    # draws new map,
    update_map()

main()