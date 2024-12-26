from models.coordinates import Coordinates
from models.search_parameters import SearchParameters
from morizon_scraper.consts import TransactionType, RealEstateType
from morizon_scraper.requests import search_map_request

warsaw_northeast_node = Coordinates(52.3679992, 21.2710984)
warsaw_southwest_node = Coordinates(52.09787672, 20.3386037)

search_parameters = SearchParameters(warsaw_northeast_node, warsaw_southwest_node,
                                     TransactionType.SALE, [RealEstateType.FLAT],
                                     "Warszawa")

warsaw_clusters = search_map_request(search_parameters)
print(warsaw_clusters)
print(len(warsaw_clusters['data']['searchMap']['markers']))
