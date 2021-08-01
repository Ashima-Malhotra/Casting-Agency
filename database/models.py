from sqlalchemy import Column, String, Integer, ForeignKey, Float, Date
from flask_sqlalchemy import SQLAlchemy
import os


database_path = os.environ['DATABASE_URL']
# database_path = 'postgresql://postgres:user@localhost:5432/casting_agency'
db = SQLAlchemy()
'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


# Association Table
actor_of_movie = db.Table('actor_of_movie',
                          Column('movie_id', Integer, ForeignKey(
                              'movies.id'), primary_key=True),
                          Column('actor_id', Integer, ForeignKey(
                              'actors.id'), primary_key=True)
                          )


class Movies(db.Model):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    release_year = Column(Integer, nullable=False)
    movie_rating = Column(Float, nullable=False)
    cast = db.relationship('Actors', secondary=actor_of_movie,
                           backref=db.backref('movies', lazy=True))

    def __init__(self, title, release_year, movie_rating):
        self.title = title
        self.release_year = release_year
        self.movie_rating = movie_rating

    def short(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_year': self.release_year
        }

    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_year': self.release_year,
            "cast": [actor.name for actor in self.cast],
            'movie_rating': self.movie_rating
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return "<Movies {} {} {} {} />".format(self.title, self.release_year, self.movie_rating)


class Actors (db.Model):
    __tablename__ = "actors"

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(256), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def short(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def long(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': [movie.title for movie in self.movies]
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return "<Actors {} {} {} />".format(self.name, self.age, self.gender)
