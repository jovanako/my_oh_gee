import os
import secrets

from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2.functions import ST_DWithin
from geoalchemy2.shape import from_shape
from geoalchemy2.types import Geography, Geometry
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.sql.expression import cast

_SRID = 4326

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
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


class Entry_Requirement(db.Model):
    __tablename__ = 'entry_requirements'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    description = Column(Text, nullable=False)


class Venue_Type(db.Model):
    __tablename__ = 'venue_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)


class Venue(db.Model):
    __tablename__ = 'venues'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    address = Column(String(100), nullable=False)
    geom = Column(Geometry(geometry_type='POINT', srid=_SRID))
    requirement_id = Column(String(100), ForeignKey(
        'entry_requirements.id'), nullable=False)
    venue_type_id = Column(String(100), ForeignKey(
        'venue_types.id'), nullable=False)
    webpage = Column(String(100))
    image_path = Column(String(100))
    creator_id = Column(String(100), ForeignKey('users.id'), nullable=False)

    # @staticmethod
    # def get_venues_within_radius(lat, lng, radius_meters):
    #     # TODO: The arbitrary limit = 100 is just a quick way to make sure
    #     # we won't return tons of entries at once,
    #     # paging needs to be in place for real usecase
    #     results = Venue.query.filter(
    #         ST_DWithin(
    #             cast(Venue.geom, Geography),
    #             cast(from_shape(Point(lng, lat)), Geography),
    #             radius_meters)
    #     ).limit(100).all()

    #     return [l.to_dict() for l in results]
