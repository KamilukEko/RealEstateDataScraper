from db.database import init_db
from models.coordinates import Coordinates
from scrapers.morizon_scraper.consts import TransactionType, RealEstateType
from scrapers.morizon_scraper.morizon_requests import search_map_request
from scrapers.morizon_scraper.search_parameters import SearchParameters
from scrapers.olx_scraper.olx_scraper import scrape_details_from_url as olx_scrape_details_from_url
from scrapers.morizon_scraper.morizon_scraper import scrape_details_from_cluster as morizon_scrape_details_from_cluster

warsaw_northeast_node = Coordinates(52.3679992, 21.2710984)
warsaw_southwest_node = Coordinates(52.09787672, 20.3386037)
search_parameters = SearchParameters(warsaw_northeast_node, warsaw_southwest_node,
                                     TransactionType.SALE, [RealEstateType.FLAT])
warsaw_clusters = search_map_request(search_parameters, 1)

init_db()

morizon_scrape_details_from_cluster(warsaw_clusters)
olx_scrape_details_from_url("https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/warszawa/?search%5Border%5D=created_at:desc", 1)





