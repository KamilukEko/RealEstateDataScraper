from schemas.offer_data_schema import OfferDataSchema


def _parse_number(value: str) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        return float(value.replace(',', '.'))
    return 0.0

def parse_morizon_property_data(data_dict: dict) -> OfferDataSchema:
    property_data = data_dict.get('data', {}).get('propertyData', {})
    company_name, company_phone, offeror_name, offeror_phone, floor = None, None, None, None, None

    if not property_data:
         raise Exception("Property data not found")

    id_val = property_data.get('id')
    address_val = property_data.get('location', {}).get('street')
    city_val = property_data.get('location', {}).get('location')[0]
    area_val = _parse_number(property_data.get('area'))
    url_val = "https://www.morizon.pl" + property_data.get('url')
    latitude_val = _parse_number(property_data.get('location', {}).get('map', {}).get('center', {}).get('latitude'))
    longitude_val = _parse_number(property_data.get('location', {}).get('map', {}).get('center', {}).get('longitude'))

    contact = property_data.get('contact')
    if contact:
        company = contact.get('company')
        if company:
            company_name = company.get('name')
            company_phone = company.get('phones', [None])[0]

        person = contact.get('person')
        if person:
            offeror_name = person.get('name')
            offeror_phone = person.get('phones', [None])[0]


    price_val = property_data.get('price')
    if price_val:
        price_val = _parse_number(price_val.get('amount'))

    floor_val = property_data.get('floorFormatted')
    if floor_val:
        floor_val = floor_val.split("/")[0]
        floor = 0 if floor_val == "parter" else int(floor_val.split()[-1])


    property_instance_data = {
        "inner_id": str(id_val),
        "url": url_val,
        "source": "MORIZON",
        "offeror_name": offeror_name,
        "offeror_phone": offeror_phone,
        'agency_name': company_name,
        'agency_phone': company_phone,
        "city": city_val,
        'floor': floor,
        "address": address_val,
        "price": price_val,
        "area": area_val,
        "latitude": latitude_val,
        "longitude": longitude_val
    }

    return OfferDataSchema(**property_instance_data)