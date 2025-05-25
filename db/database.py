from datetime import datetime
from sqlalchemy import exists

from db.models.agency import Agency
from db.models.property import Property
from db.models.offer import Offer
from db.models.offeror import Offeror
from db.models.offer_update import OfferUpdate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models.base import Base
from schemas.offer_data_schema import OfferDataSchema
from sqlalchemy import or_, and_

engine = create_engine('sqlite:///real_estate.db')
SessionLocal = sessionmaker(bind=engine)

def init_db():
    import db.models.property
    import db.models.offer
    import db.models.agency
    import db.models.offeror
    import db.models.offer_update
    Base.metadata.create_all(bind=engine)


def add_property(property_data: OfferDataSchema, session: SessionLocal):
    exists_query = session.query(exists().where(
        and_(Property.longitude == property_data.longitude,
             Property.latitude == property_data.latitude,
             Property.area == property_data.area)
    )).scalar()

    if exists_query:
        property_obj = session.query(Property).filter(
            and_(Property.longitude == property_data.longitude,
                 Property.latitude == property_data.latitude,
                 Property.area == property_data.area)
        ).first()
    else:
        property_obj = Property(
            address=property_data.address,
            city=property_data.city,
            area=property_data.area,
            floor=property_data.floor,
            latitude=property_data.latitude,
            longitude=property_data.longitude
        )
        session.add(property_obj)
        session.flush()

    return property_obj


def add_agency(property_data: OfferDataSchema, session):
    exists_query = session.query(exists().where(
        Agency.name == property_data.agency_name,
            Agency.email == property_data.agency_email,
            Agency.phone == property_data.agency_phone,
    )).scalar()

    if exists_query:
        agency_obj = session.query(Agency).filter(
            Agency.name == property_data.agency_name,
            Agency.email == property_data.agency_email,
            Agency.phone == property_data.agency_phone,
        ).first()
    else:
        agency_obj = Agency(
            source=property_data.source,
            name=property_data.agency_name,
            email=property_data.agency_email,
            phone=property_data.agency_phone,
        )
        session.add(agency_obj)
        session.flush()

    return agency_obj

def add_offeror(property_data: OfferDataSchema, agency_id, session):
    exists_query = session.query(exists().where(
        Offeror.name == property_data.offeror_name,
            Offeror.inner_id==property_data.offeror_id,
            Offeror.agency_id==agency_id
    )).scalar()

    if exists_query:
        offeror_obj = session.query(Offeror).filter(
            Offeror.name == property_data.offeror_name,
            Offeror.inner_id==property_data.offeror_id,
            Offeror.agency_id == agency_id
        ).first()
    else:
        offeror_obj = Offeror(
            name=property_data.offeror_name,
            source=property_data.source,
            inner_id=property_data.offeror_id,
            phone=property_data.offeror_phone,
            agency_id=agency_id
        )
        session.add(offeror_obj)
        session.flush()

    return offeror_obj

def offer_exists(property_data: OfferDataSchema, session):
    exists_query = session.query(exists().where(
        Offer.inner_id == property_data.inner_id,
        Offer.url == property_data.url,
        Offer.source == property_data.source
    )).scalar()
    return exists_query

def get_offer(property_data: OfferDataSchema, session):
    return session.query(Offer).filter(
        Offer.inner_id == property_data.inner_id,
        Offer.source == property_data.source
    ).first()

def add_offer(property_data: OfferDataSchema, offeror_id, property_id, session):
    if offer_exists(property_data, session):
        return get_offer(property_data, session)
    else:
        offer_obj = Offer(
            inner_id=property_data.inner_id,
            offeror_id=offeror_id,
            property_id=property_id,
            url=property_data.url,
            source=property_data.source,
            offer_date=datetime.now()
        )
        session.add(offer_obj)
        session.flush()

    return offer_obj

def add_update(property_data: OfferDataSchema, offer_id, session):
    update_obj = OfferUpdate(
        update_date=datetime.now(),
        price=property_data.price,
        offer_id=offer_id
    )
    session.add(update_obj)
    session.flush()
    session.commit()
    return update_obj

def update_existing_offer(property_data: OfferDataSchema, session):
    offer_obj = get_offer(property_data, session)

    last_update = session.query(OfferUpdate).filter(
        OfferUpdate.offer_id == offer_obj.id
    ).order_by(OfferUpdate.update_date.desc()).first()

    if property_data.price == last_update.price:
        return f"Offer does not require an update: {property_data.url}"

    update_obj = add_update(property_data, offer_obj.id, session)
    update_obj.offer = offer_obj

    return f"Updated offer: {property_data.url}"

def handle_data(property_data: OfferDataSchema):
    session = SessionLocal()
    try:
        if offer_exists(property_data, session):
            return update_existing_offer(property_data, session)

        property_obj = add_property(property_data, session)

        agency_obj = None
        if property_data.agency_name:
            agency_obj = add_agency(property_data, session)

        offeror_obj = add_offeror(property_data, (agency_obj.id if agency_obj is not None else None), session)
        offeror_obj.agency = agency_obj

        offer_obj = add_offer(property_data, offeror_obj.id, property_obj.id, session)
        offer_obj.property = property_obj
        offer_obj.offeror = offeror_obj

        update_obj = add_update(property_data, offer_obj.id, session)
        update_obj.offer = offer_obj

        return f"Added new offer: {property_data.url}"

    except Exception as e:
        session.rollback()
        return f"Error: {str(e)}"
    finally:
        session.close()

