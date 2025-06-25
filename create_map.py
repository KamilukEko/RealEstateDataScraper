import folium
import pandas as pd
from sqlalchemy.orm import sessionmaker, joinedload
from db.database import engine
from db.models.property import Property
from db.models.offer import Offer

def get_properties_from_db():
    session = sessionmaker(bind=engine)()
    try:
        properties = session.query(Property).options(
                joinedload(Property.offers)
                .joinedload(Offer.updates)
            ).all()
        return properties
    finally:
        session.close()

def create_map(properties_data, save_path="warsaw_map.html"):
    warsaw_coords = [52.2297, 21.0122]

    m = folium.Map(location=warsaw_coords, zoom_start=11)
    df = pd.DataFrame([{
        'id': prop.id,
        'area': prop.area,
        'floor': prop.floor,
        'latitude': prop.latitude,
        'longitude': prop.longitude,
        'city': prop.city,
        'address': prop.address,
        'offers': [
            {
                'offer_id': offer.id,
                'inner_id': offer.inner_id,
                'source': offer.source,
                'date': offer.offer_date.strftime('%Y-%m-%d'),
                'url': offer.url,
                'prices': [
                    {
                        'price': update.price,
                        'update_date': update.update_date.strftime('%d-%m-%Y')
                    }
                    for update in offer.updates
                ]
                if offer.updates else None
            }
            for offer in prop.offers
        ] if prop.offers else None,
    } for prop in properties_data])

    df['price'] = df['offers'].apply(lambda x: min(
        [update['price']
         for offer in x
         for update in offer['prices']
         if update['price'] is not None],
        default=None
    ) if x and any(offer['prices'] for offer in x if offer['prices']) else None)
    df['price_per_m2'] = df.apply(lambda x: x['price'] / x['area'] if x['price'] is not None else None, axis=1)

    price_per_m2_range = [
        (None, None, 'gray'),
        (0, 10000, 'green'),
        (10000, 15000, 'blue'),
        (15000, 20000, 'yellow'),
        (20000, 25000, 'orange'),
        (25000, float('inf'), 'red')
    ]

    for min_price, max_price, color in price_per_m2_range:
        if color == 'gray':
            filtered_props = df[df['price_per_m2'].isna()]
        else:
            filtered_props = df[(df['price_per_m2'] >= min_price) & (df['price_per_m2'] < max_price)]

        if not filtered_props.empty:
            m2_feature_group = folium.FeatureGroup(name=f"{min_price}-{max_price} zł per m² properties ({len(filtered_props)})")

            for _, prop in filtered_props.iterrows():
                folium.CircleMarker(
                    location=[prop['latitude'], prop['longitude']],
                    radius=8,
                    popup=folium.Popup(
                        f"""
                        <div style="white-space: pre;">
                        <b>Price:</b> {prop['price'] or 'N/A'} zł<br>
                        <b>Area:</b> {prop['area']}m²<br>
                        {f"<b>Price per m²:</b> {prop['price_per_m2']:.2f} zł<br>" if prop['price'] is not None else ''}
                        <b>Floor:</b> {prop['floor'] or 'N/A'}<br>
                        <b>Address:</b> {prop['address'] or 'Not specified'}<br>
                        <b>Offers:</b><br>
                        {
                        '<br>'.join(
                            f"&nbsp;&nbsp;&nbsp;&nbsp;<a href='{offer['url']}' target='_blank'>{offer['source']}({offer['inner_id']}) from {offer['date']}</a>" +
                            '<br>' +
                            '<br>'.join(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{price['update_date']}: {price['price']} zł"
                                        for price in offer['prices'])
                            for offer in prop['offers']
                        ) if prop['offers'] else ''
                        }
                        </div>
                        """,
                        max_width=300,
                        min_width=150
                    ),
                    color=color,
                    fill=True,
                    fillColor=color,
                    fillOpacity=0.7
                ).add_to(m2_feature_group)

            m2_feature_group.add_to(m)

    folium.LayerControl().add_to(m)
    m.save(save_path)
    print(f"Advanced map saved to {save_path}")

    return m

if __name__ == "__main__":
    properties = get_properties_from_db()
    map_advanced = create_map(properties, "warsaw_advanced.html")
    print("Maps created successfully!")