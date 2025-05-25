from schemas.offer_data_schema import OfferDataSchema


def parse_olx_property_data(data_dict: dict) -> OfferDataSchema:
    property_instance_data = {
        "inner_id": data_dict['id'],
        "url": data_dict['url'],
        "offeror_name": data_dict['username'],
        "offeror_id": data_dict['offeror_id'],
        'floor': data_dict['floor'],
        "source": "OLX",
        "price": data_dict['price'],
        "area": data_dict['area'],
        "latitude": data_dict['latitude'],
        "longitude": data_dict['longitude']
    }

    return OfferDataSchema(**property_instance_data)

