import json

from models.coordinates import Coordinates
from models.search_parameters import SearchParameters
from morizon_scraper.consts import TransactionType, RealEstateType
from morizon_scraper.requests import search_map_request, get_property_cluster_data_request, get_property_details_request

warsaw_northeast_node = Coordinates(52.3679992, 21.2710984)
warsaw_southwest_node = Coordinates(52.09787672, 20.3386037)

search_parameters = SearchParameters(warsaw_northeast_node, warsaw_southwest_node,
                                     TransactionType.SALE, [RealEstateType.FLAT],
                                     "Warszawa")

warsaw_clusters = search_map_request(search_parameters)

real_estates = []

for cluster in warsaw_clusters['data']['searchMap']['markers']:
    property_cluster = get_property_cluster_data_request(cluster['url'])
    for real_estate in property_cluster['data']['searchResult']['properties']['nodes']:
        real_estates.append(get_property_details_request(real_estate['url']))

with open("real_estates.json", "w") as f:
    json.dump(real_estates, f, indent=4)




