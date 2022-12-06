from pymongo import MongoClient

from Utilities import Utilities


employees_validator = {
    'validator': {
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ["first_name", "last_name"],
            'additionalProperties': False,
            'properties': {
                '_id': {},
                'first_name': {
                    'bsonType': "string"
                },
                'last_name': {
                    'bsonType': "string"
                },
                'balance': {
                    'bsonType': "int"
                }
            }
        }
    }
}
requests_validator = {
    'validator': {
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ["room_number", "employee_id"],
            'additionalProperties': False,
            'properties': {
                '_id': {},
                'employee_id': {
                    'bsonType': 'object'
                },
                'room_number': {},
                'building_name': {},
                'date_requested': {
                    'bsonType': 'date'
                }
            }
        }
    }
}
buildings_validator = {
    'validator': {
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ["building_name"],
            'additionalProperties': False,
            'properties': {
                '_id': {},
                'building_name': {}
            }
        }
    }
}
rooms_validator = {
    'validator': {
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ["room_number", "building_name"],
            'additionalProperties': False,
            'properties': {
                '_id': {},
                'room_number': {},
                'building_name': {}
            }
        }
    }
}
doors_validator = {
    'validator': {
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ["door_name", "room_number", "building_name"],
            'additionalProperties': False,
            'properties': {
                '_id': {},
                'door_name': {

                },
                'room_number': {},
                'building_name': {}
            }
        }
    }
}
hooks_validator = {
    'validator': {
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ["hook_id"],
            'additionalProperties': False,
            'properties': {
                '_id': {
                    'bsonType': 'int',
                    "Description": "Yea that's it, just the id"
                }
            }
        }
    }
}
keys_validator = {
        'validator': {
            '$jsonSchema': {
                'bsonType': "object",
                'description': "Key issued to employees to open doors",
                'required': ["door_name", "room_number", "building_name", "hook_id"],
                'additionalProperties': False,
                'properties': {
                    '_id': {
                        'bsonType': "int",
                        "description": "lmao, i hope this works"
                    },
                    'door_name': {
                        'bsonType': "string",
                        "description": "name of the door correlating to locations"
                    },
                    'room_number': {
                        'bsonType': "int",
                        "description": "number assigned to the room",
                    },
                    'building_name': {
                        'bsonType': "string",
                        "description": "name of the building the room is in"
                    },
                    'hook_id': {
                        'bsonType': "object",
                        "description": "id of the hook the key is a copy of"
                    }
                }
            }
        }
    }
issued_keys_validator = {
    'validator': {
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ["request_id", "key_id", "date_due_back"],
            'additionalProperties': False,
            'properties': {
                '_id': {},
                'request_id': {
                    'bsonType': 'object',
                    "description": "migrating key of the corresponding request"
                },
                'key_id': {
                    'bsonType': 'object',
                    "description": "migrating key of the keys"
                },
                'date_due_back': {
                    'bsonType': 'date',
                    "description": "Date the issued key is due back"
                },
                'date_returned': {
                    'bsonType': 'date',
                    "description": "Date the issued key was returned"
                },
                'date_reported_lost': {
                    'bsonType': 'date',
                    "description": "Date the key was reported lost, usually null"
                }
            }
        }
    }
}
