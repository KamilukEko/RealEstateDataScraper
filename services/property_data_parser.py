from schemas.property_schema import PropertySchema

def _parse_number(value: str) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        return float(value.replace(',', '.'))
    return 0.0

def parse_olx_property_data(data_dict: dict) -> PropertySchema:
    property_instance_data = {
        "inner_id": data_dict['id'],
        "url": data_dict['url'],
        "contact": data_dict['username'],
        "source": "OLX",
        "price": data_dict['price'],
        "area": data_dict['area'],
        "latitude": data_dict['latitude'],
        "longitude": data_dict['longitude']
    }

    return PropertySchema(**property_instance_data)

def parse_morizon_property_data(data_dict: dict) -> PropertySchema:
    property_data = data_dict.get('data', {}).get('propertyData', {})

    if not property_data:
         raise Exception("Property data not found")

    id_val = property_data.get('id')
    address_val = property_data.get('location', {}).get('street')
    city_val = property_data.get('location', {}).get('location')[0]
    area_val = _parse_number(property_data.get('area'))
    url_val = "https://www.morizon.pl" + property_data.get('url')
    latitude_val = _parse_number(property_data.get('location', {}).get('map', {}).get('center', {}).get('latitude'))
    longitude_val = _parse_number(property_data.get('location', {}).get('map', {}).get('center', {}).get('longitude'))

    contact_name = None
    contact = property_data.get('contact')
    if contact:
        company = contact.get('company')
        if company:
            contact_name = company.get('name')

    price_val = property_data.get('price')
    if price_val:
        price_val = _parse_number(price_val.get('amount'))

    property_instance_data = {
        "inner_id": str(id_val),
        "url": url_val,
        "source": "MORIZON",
        "contact": contact_name,
        "city": city_val,
        "address": address_val,
        "price": price_val,
        "area": area_val,
        "latitude": latitude_val,
        "longitude": longitude_val
    }

    return PropertySchema(**property_instance_data)