import os
import secrets

from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2.functions import ST_DWithin
from geoalchemy2.shape import from_shape, to_shape
from geoalchemy2.types import Geography, Geometry
from shapely.geometry import Point
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.sql.expression import cast

_SRID = 4326
ANY_VENUE_TYPE_ID = 0
ANY_ENTRY_REQUIREMENT_ID = 0

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


def set_up_db(app):
    database_path = os.getenv('DATABASE_URL', 'DATABASE_URL_WAS_NOT_SET?!')
    database_path = database_path.replace('postgres://', 'postgresql://')
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY'] = secrets.token_hex()
    db.app = app
    db.init_app(app)
    db.create_all()
    login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(60), nullable=False)


class EntryRequirement(db.Model):
    __tablename__ = 'entry_requirements'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    description = Column(Text, nullable=False)


class VenueType(db.Model):
    __tablename__ = 'venue_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)


class Venue(db.Model):
    __tablename__ = 'venues'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    address = Column(String(100), nullable=False)
    geom = Column(Geometry(geometry_type='POINT', srid=_SRID), nullable=False)
    requirement_id = Column(Integer, ForeignKey(
        'entry_requirements.id'), nullable=False)
    requirement = db.relationship('EntryRequirement')
    venue_type_id = Column(Integer, ForeignKey(
        'venue_types.id'), nullable=False)
    venue_type = db.relationship('VenueType')
    webpage = Column(String(100))
    image_path = Column(String(100))
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    creator = db.relationship('User')

    def get_location_latitude(self):
        point = to_shape(self.geom)
        return point.x

    def get_location_longitude(self):
        point = to_shape(self.geom)
        return point.y

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'location': {
                'lat': self.get_location_latitude(),
                'lng': self.get_location_longitude()
            },
            'requirement': self.requirement.name,
            'requirementDescription': self.requirement.description,
            'webpage': self.webpage,
            'imagePath': self.image_path
        }

    @staticmethod
    def save(venue):
        db.session.add(venue)
        db.session.commit()

    @staticmethod
    def get_venues_in_vicinity(lat, lng, search, venue_type_id, entry_requirement_id):
        query = Venue.query

        if lat is not None and lng is not None:
            query.filter(ST_DWithin(
                cast(Venue.geom, Geography),
                cast(from_shape(Point(lng, lat)), Geography),
                3000))

        venue_type_id = ANY_VENUE_TYPE_ID if venue_type_id is None else venue_type_id
        if venue_type_id is not ANY_VENUE_TYPE_ID:
            query = query.filter_by(venue_type_id=venue_type_id)

        entry_requirement_id = ANY_ENTRY_REQUIREMENT_ID if entry_requirement_id is None else entry_requirement_id
        if entry_requirement_id is not ANY_ENTRY_REQUIREMENT_ID:
            query = query.filter_by(requirement_id=entry_requirement_id)

        if search != '' and search is not None:
            query = query.filter(Venue.name.ilike(f'%{search}%'))

        return query.limit(100).all()
