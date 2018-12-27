from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'email': self.email,
            'picture': self.picture,

        }


class NovelsCategories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class Items(Base):
    __tablename__ = 'items'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(500))
    price = Column(String(8))
    author = Column(String(250))
    novelType = Column(String(250))
    novelPicture = Column(String(250))
    categories_id = Column(Integer, ForeignKey('categories.id'))
    categories = relationship("NovelsCategories",
                         backref=backref("items",cascade="all, delete-orphan")
                    )
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {

            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'novelType': self.novelType,
            'author': self.author,
            'novelPicture': self.novelPicture,
            'categories_id': self.categories_id,
            'user_id': self.user_id,
        }


engine = create_engine('sqlite:///novelscategories.db')


Base.metadata.create_all(engine)
