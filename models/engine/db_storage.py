#!/usr/bin/python3
"""
Contains the class DBStorage
"""

from models.user import User
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os import getenv

classes = {'User': User}


class DBStorage:
    """Interacts with MYSQL database using sqlalchemy"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        USER = getenv('USER')
        PWD = getenv('PWD')
        HOST = getenv('HOST')
        DB = getenv('DB')
        # ENV = getenv('ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(USER, PWD, HOST, DB))

    def all(self, cls=None):
        """Query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self, obj):
        """Commit all changes to the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reload data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def get(self, cls, id):
        """Returns the object based on the class name and its ID
        or None if not found"""
        if cls not in classes.values():
            return None

        all_cls = self.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value
        return None
    
    def get_user_by_username(self, username):
        """Fetch user from db by username"""
        return self.__session.query(User).filter_by(username=username).first()
    
    def add_user(self, user):
        """Adding user to db"""
        self.new(user)
        self.save()
