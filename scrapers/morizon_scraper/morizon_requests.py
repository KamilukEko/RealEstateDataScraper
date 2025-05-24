import requests

from scrapers.morizon_scraper.search_parameters import SearchParameters
from scrapers.morizon_scraper.consts import API_URL, HEADER
from scrapers.morizon_scraper.queries import create_search_map_query, create_get_property_cluster_data_query, \
    create_get_property_details_query


def search_map_request(search_parameters: SearchParameters, number_of_markers: int = 20000):
    return perform_request(create_search_map_query(search_parameters, number_of_markers))


def get_property_cluster_data_request(cluster_url: str):
    return perform_request(create_get_property_cluster_data_query(cluster_url))


def get_property_details_request(property_url: str):
    return perform_request(create_get_property_details_query(property_url))


def perform_request(payload):
    try:
        response = requests.post(API_URL, json=payload, headers=HEADER)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
