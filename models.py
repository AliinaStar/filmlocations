from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    role = Column(Enum('user', 'admin', name='role_enum'), default='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        assert self.password_hash.startswith("pbkdf2:"), "Password hash is not generated correctly"

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_user(self):
        return self.role == 'user'
"""
class User(Person):
    __tablename__ = 'users'
    
    id = Column(Integer, ForeignKey('persons.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'user'
    }
    
    def viewLocation(self, location):
        # Логіка перегляду локації
        pass
        
    def searchByAddress(self, address: str):
        # Логіка пошуку за адресою
        pass
        
    def rateLocation(self, rating: int):
        # Логіка оцінювання локації
        pass
        
    def leaveReview(self, location, text: str):
        # Логіка створення відгуку
        pass
        
    def searchByMovie(self, movie: str):
        # Логіка пошуку за фільмом
        pass
        
    def addToFavorites(self, location):
        # Логіка додавання до улюблених
        pass
        
    def viewFilm(self, film):
        # Логіка перегляду фільму
        pass

class Admin(Person):
    __tablename__ = 'admins'
    
    id = Column(Integer, ForeignKey('persons.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }
    
    def reviewProposedLocations(self):
        # Логіка перегляду запропонованих локацій
        pass
        
    def addLocation(self, location):
        # Логіка додавання локації
        pass
        
    def deleteLocation(self, location):
        # Логіка видалення локації
        pass
        
    def addLocationToFilm(self, film, location):
        # Логіка додавання локації до фільму
        pass
        
    def addFilm(self):
        # Логіка додавання фільму
        pass
"""
'''class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="favorites")
    locations = relationship("Location", secondary="favorites_locations")

    def viewList(self):
        pass

    def removeLocation(self, location):
        pass

    def checkLocationPresence(self, location):
        pass

# Таблиця для зв'язку many-to-many між Favorites і Location
favorites_locations = db.Table('favorites_locations',
    Column('favorites_id', Integer, ForeignKey('favorites.id')),
    Column('location_id', Integer, ForeignKey('locations.id'))
)

class Review(db.Model):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))
    
    user = relationship("User", back_populates="reviews")
    location = relationship("Location", back_populates="reviews")

    def createReview(self):
        pass

    def editReview(self):
        pass

    def deleteReview(self):
        pass

class ProposedLocation(db.Model):
    __tablename__ = 'proposed_locations'
    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False)
    proposed_by_id = Column(Integer, ForeignKey('users.id'))
    
    proposed_by = relationship("User", back_populates="proposed_locations")

    def proposeLocation(self, user):
        pass

    def approveRejectLocation(self, admin):
        pass

    def editProposedLocation(self):
        pass

class Location(db.Model):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    description = Column(String)
    rating = Column(Integer, nullable=True)  # None є допустимим значенням
    photo = Column(LargeBinary)  # BLOB для зберігання фото
    sharingAddress = Column(String)
    
    reviews = relationship("Review", back_populates="location")
    films = relationship("Film", secondary="film_locations")

    def addPhoto(self, blob):
        pass

    def updateRating(self, rating):
        pass

    def edit(self):
        pass

class Film(db.Model):
    __tablename__ = 'films'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    year = Column(Integer)
    description = Column(String)
    ratingIMDb = Column(Integer)
    
    locations = relationship("Location", secondary="film_locations")

# Таблиця для зв'язку many-to-many між Film і Location
film_locations = db.Table('film_locations',
    Column('film_id', Integer, ForeignKey('films.id')),
    Column('location_id', Integer, ForeignKey('locations.id'))
)'''