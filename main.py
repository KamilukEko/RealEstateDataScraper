from db.database import init_db, SessionLocal
from db.models.property import Property
from models.coordinates import Coordinates
from scrapers.morizon_scraper.search_parameters import SearchParameters
from scrapers.morizon_scraper.consts import TransactionType, RealEstateType
from scrapers.morizon_scraper.morizon_requests import search_map_request, get_property_cluster_data_request, get_property_details_request
from services.property_data_parser import parse_morizon_property_data, parse_olx_property_data
from scrapers.olx_scraper.olx_scraper import get_all_offers_from_url, extract_data_from_offers

warsaw_northeast_node = Coordinates(52.3679992, 21.2710984)
warsaw_southwest_node = Coordinates(52.09787672, 20.3386037)

search_parameters = SearchParameters(warsaw_northeast_node, warsaw_southwest_node,
                                     TransactionType.SALE, [RealEstateType.FLAT],
                                     "Warszawa")

warsaw_clusters = search_map_request(search_parameters, 1)

init_db()
session = SessionLocal()

for cluster in warsaw_clusters['data']['searchMap']['markers']:
    property_cluster = get_property_cluster_data_request(cluster['url'])
    for real_estate in property_cluster['data']['searchResult']['properties']['nodes']:
        property_schema = parse_morizon_property_data(get_property_details_request(real_estate['url']))
        property_data = Property(**property_schema.model_dump())
        session.add(property_data)
        print(f"Added property: {property_data.url}")

urls = get_all_offers_from_url("https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/sosnowiec/?search%5Bfilter_enum_rooms%5D%5B0%5D=one")
olx_properties = extract_data_from_offers(urls)

for olx_property in olx_properties:
    property_schema = parse_olx_property_data(olx_property)
    property_data = Property(**property_schema.model_dump())
    session.add(property_data)

session.commit()
session.close()




