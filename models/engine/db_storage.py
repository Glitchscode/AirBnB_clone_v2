#!/usr/bin/python3
""" Database Storage"""
from os import getenv
from models.base_model import BaseModel, Base
from models.user import User
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (create_engine)
from sqlalchemy.orm import scoped_session



class DBStorage:
    """
    """
    __engine = None
    __session = None
    def __init__(self):
        """
        """
        username = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db_name = getenv("HBNB_MYSQL_DB")

        db_url = "mysql+mysqldb://{}:{}@{}/{}".format(username, password, host, db_name)
        self.__engine = create_engine(db_url, pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Makes a query to the database
        if cls is given, query for cls only else query for all"""
        objs = []
        if cls is None:
            Classes = [User, City, State, Place, Review, Amenity]
            try:
                for Class in Classes:
                    objs = objs + self.__session.query(Class).all()
            except Exception:
                pass
        else:
            obj_dict = {}
            Class = eval(cls) if type(cls) == str else cls
            objs = self.__session.query(Class).all()
            for o in objs:
                key = "{}.{}".format(o.__class__.__name__, o.id)
                if o.__class__.__name__ == 'State' or o.__class__.__name__ == 'City':
                    del o._sa_instance_state
                    obj_dict[key] = o
                else:
                    obj_dict[key] = o

        return obj_dict

    def new(self, obj):
        """Adds the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session()
