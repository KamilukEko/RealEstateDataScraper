from models.coordinates import Coordinates
from models.search_parameters import SearchParameters
from morizon_scraper.consts import TransactionType, RealEstateType
from morizon_scraper.requests import search_map_request, get_property_cluster_data_request, get_property_details_request

warsaw_northeast_node = Coordinates(52.3679992, 21.2710984)
warsaw_southwest_node = Coordinates(52.09787672, 20.3386037)

search_parameters = SearchParameters(warsaw_northeast_node, warsaw_southwest_node,
                                     TransactionType.SALE, [RealEstateType.FLAT],
                                     "Warszawa")

warsaw_clusters = search_map_request(search_parameters, 1)

property_cluster = get_property_cluster_data_request(warsaw_clusters['data']['searchMap']['markers'][0]['url'])
real_estate = get_property_details_request(property_cluster['data']['searchResult']['properties']['nodes'][0]['url'])

print(property_cluster)
print(real_estate)




