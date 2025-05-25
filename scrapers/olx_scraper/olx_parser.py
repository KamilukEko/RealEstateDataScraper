from schemas.property_schema import PropertySchema


def parse_olx_property_data(data_dict: dict) -> PropertySchema:
    property_instance_data = {
        "inner_id": data_dict['id'],
        "url": data_dict['url'],
        "offeror_name": data_dict['username'],
        "offeror_type": data_dict['offeror_type'],
        "offeror_id": data_dict['offeror_id'],
        "source": "OLX",
        "price": data_dict['price'],
        "area": data_dict['area'],
        "latitude": data_dict['latitude'],
        "longitude": data_dict['longitude']
    }

    return PropertySchema(**property_instance_data)

