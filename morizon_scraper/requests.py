import requests

from models.search_parameters import SearchParameters
from morizon_scraper.consts import API_URL, HEADER
from morizon_scraper.queries import create_search_map_query


def search_map_request(search_parameters: SearchParameters, number_of_markers: int = 20000):
    return perform_request(create_search_map_query(search_parameters, number_of_markers))


def perform_request(payload):
    try:
        response = requests.post(API_URL, json=payload, headers=HEADER)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
