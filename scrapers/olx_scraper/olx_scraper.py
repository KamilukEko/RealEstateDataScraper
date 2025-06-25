import argparse
import json
from itertools import count
from urllib.parse import urlparse
import bs4 as bs

import requests

import db.database
from scrapers.olx_scraper.consts import HEADERS, OLX_OFFER_PATTERN, OLX_BASE_URL
from scrapers.olx_scraper.olx_parser import parse_olx_property_data


def get_all_offers_from_url(url, page_limit=100000):
    parsed_url = urlparse(url)

    if not parsed_url.query:
        marker = '?'
    else:
        marker = '&'

    total_urls = []
    for index in count(0):
        if index >= page_limit:
            break

        if not index:
            url_page = url
        else:
            current_page = '{}page={}'.format(marker, index)
            url_page = url + current_page

        urls = get_all_offers_from_page(url_page)
        if not urls:
            break

        total_urls.extend(urls)

    return sorted(set(total_urls))


def get_all_offers_from_page(url):
    try:
        res = requests.get(url, headers=HEADERS)
    except Exception as e:
        print(f'Exception in - {url}: {e}')
        return []

    if res.status_code != 200:
        print(f'Error: {res.status_code} - {url}')
        return []

    soup = bs.BeautifulSoup(res.text, 'lxml')
    offers_div = soup.find('div', {'data-testid': "listing-grid"})
    offers = offers_div.find_all('div', {'data-cy': "l-card"})


    urls = []
    for offer in offers:
        url = offer.a['href']
        if url.startswith(OLX_OFFER_PATTERN):
            url = OLX_BASE_URL + url
        urls.append(url)

    return urls


def extract_data_from_offers(urls):
    extracted_data = []
    for url in urls:
        try:
            details = get_offer_details(url)
            if not details:
                continue

            price, id, username, offeror_type, offeror_id, area, latitude, longitude, floor = details
            extracted_data.append({
                'url': url,
                'id': id,
                'username': username,
                'offeror_type': offeror_type,
                'offeror_id': offeror_id,
                'price': price,
                'area': area,
                'floor': floor,
                'latitude': latitude,
                'longitude': longitude
            })
        except Exception as e:
            print(f"Error extracting data from - {url}: {e}", e)
            continue
    return extracted_data


def get_offer_details(url):
    res = requests.get(url, headers=HEADERS)
    soup = bs.BeautifulSoup(res.text, 'lxml')

    price, id, username, offeror_type, offeror_id, area, latitude, longitude, floor = (0, '', '', '', '', 0, 0, 0, 0)
    if url.startswith(OLX_BASE_URL):
        price_container = soup.find('div', {'data-testid': "ad-price-container"})
        if price_container is not None:
            price = price_container.h3.text
            price = float(''.join(price.rstrip('zł ').replace(',', '.').split()))

        parameters_container = soup.find('div', {'data-testid': "ad-parameters-container"})
        if parameters_container is None:
            return False

        area_element = parameters_container.find('p', string=lambda x: x and 'Powierzchnia:' in x)
        if not area_element:
            return False

        area_text = area_element.text.replace(',', '.')
        area = float(''.join([c for c in area_text if (c.isdigit() or c == '.') and c != '²']))

        floor_element = parameters_container.find('p', string=lambda x: x and 'Poziom:' in x)
        if floor_element:
            floor = floor_element.text.replace('Poziom: ', '')
            floor = int(floor) if floor.isdecimal() else 0

        username_element = soup.find('h4', {'data-testid': 'user-profile-user-name'})
        if not username_element:
            return False

        username = username_element.text.strip()

        footer_section = soup.find('div', {'data-testid': "ad-footer-bar-section"})
        if not footer_section:
            return False

        id_span = footer_section.find('span')
        if not id_span:
            return False
        id = ''.join(filter(str.isdigit, id_span.text))

        offeror_type_p = soup.find('p', {'data-testid': "trader-title"})
        if offeror_type_p:
            if offeror_type_p.text.strip() == 'Osoba prywatna':
                pass # TODO: Get data about agency

        offeror_url_element = soup.find('a', {'data-testid': "user-profile-link"})
        if not offeror_url_element:
            return False
        offeror_id = offeror_url_element['href'].split('/')[-2]

        config_script = soup.find('script', {'id': "olx-init-config"})
        config_script_lines = config_script.text.splitlines()
        pattern = 'window.__PRERENDERED_STATE__'
        geo_line = ''
        for line in config_script_lines:
            if line.strip().startswith(pattern):
                geo_line = line
        if not geo_line:
            print('no geo data')

        js_variable = geo_line.rstrip(';').split('= ', 1)[1]
        js_var_dict = json.loads(js_variable)
        js_var_dict = json.loads(js_var_dict)
        map_data = js_var_dict['ad']['ad']['map']
        latitude = map_data.get('lat', 0)
        longitude = map_data.get('lon', 0)

    if not any((price, id, offeror_type, offeror_id, username, area, latitude, longitude, floor)):
        return False

    return price, id, username, offeror_type, offeror_id, area, latitude, longitude, floor

def scrape_details_from_url(url, page_limit=100000):
    urls = get_all_offers_from_url(url, page_limit)
    olx_properties = extract_data_from_offers(urls)

    is_agency = True if 'private_business%5D=business' in url else False

    for olx_property in olx_properties:
        property_schema = parse_olx_property_data(olx_property, is_agency)
        print(db.database.handle_data(property_schema))
