#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.user import User

classes = {"User": User}


class FileStorage:
    """
    Serializes instances to JSON file &
    deserializes JSON back to instances
    """
    # string - path to JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """Returns the dictionary __objects if cls is None or
        new_dict if cls is not None"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """Add obj to __objects with key <obj class name>.id"""
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """Serializes __objects to JSON file"""
        json_objects = {}

        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                json_objs = json.load(f)
            for key in json_objs:
                self.__objects[key] = \
                    classes[json_objs[key]["__class__"]](**json_objs[key])
        except Exception:
            pass

    def delete(self, obj=None):
        """Delete obj from __objects"""
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in self.__objects:
                del self.__objects[obj]

    def close(self):
        """Call reload() method for deserializing the JSON file to objects"""
        self.reload

    def get_username(self, cls, username):
        """Returns the object based on the class name and its username
        or None if not found"""
        if cls not in classes.values():
            return None

        all_cls = self.all(cls)
        for value in all_cls.values():
            if (value.username == username):
                return value
        return None

    def get_email(self, cls, email):
        """Returns the object based on the class name and its username
        or None if not found"""
        if cls not in classes.values():
            return None

        all_cls = self.all(cls)
        for value in all_cls.values():
            if (value.email == email):
                return value
        return None
