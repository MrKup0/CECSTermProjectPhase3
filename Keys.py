import getpass
from datetime import datetime
from pprint import pprint

import pymongo
from bson import DBRef
from pymongo import MongoClient
from pprint import pprint
from Utilities import Utilities

Keys_validator = {
    'validator': {
        '$jsonSchema': {
            # Signifies that this schema is complex, has parameters within it.
            # These can be nested.
            'bsonType': "object",
            'description': "Creates a key needed to enter a specific room",
            'required': ["hook_id", "room_number", "door_name"],
            'additionalProperties': False,
            'properties': {
                # I would LIKE to demand an ObjectID here, but I cannot figure out how
                'hook_id': {},
                'name': {
                    'bsonType': "Integer",
                    "description": "Id of the key that will be called upon when asked."
                },
                'room_number': {
                    # the type "number" matches integer, decimal, double, and long
                    'bsonType': "Integer",
                    "description": "the room number that the key will be matched too",
                },
                'door_name': {
                    'bsonType': "String",
                    "description": "Name of the class that is inside the room"
                                   'bsonType': "string"
                },
                'active': {
                    'bsonType': "bool",
                    "description": "Do we still offer this pizza?"
                },
                'description': {
                    'bsonType': "string",
                    "description": "Mouth-watering text to show customer what to buy"
                }
db.command('collMod', 'pizza_M2M', **Keys_validator)





