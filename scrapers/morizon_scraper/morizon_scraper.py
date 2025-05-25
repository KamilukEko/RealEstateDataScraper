import db.database
from scrapers.morizon_scraper.morizon_requests import get_property_cluster_data_request, get_property_details_request
from scrapers.morizon_scraper.morizon_parser import parse_morizon_property_data


def scrape_details_from_cluster(clusters):
    for cluster in clusters['data']['searchMap']['markers']:
        property_cluster = get_property_cluster_data_request(cluster['url'])
        for real_estate in property_cluster['data']['searchResult']['properties']['nodes']:
            property_schema = parse_morizon_property_data(get_property_details_request(real_estate['url']))
            print(db.database.add_or_update_property(property_schema))