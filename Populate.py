from datetime import datetime

from pymongo import MongoClient
import Validators
from bson import DBRef

# Establish Connection
cluster = "mongodb+srv://Kupo:001657916579@termproject.7grkfgp.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(cluster)
db = client.Term_Project

# Populate Employees
employees = db.employees

employees.insert_many([
    {"_id": 1234, "first_name": "John", "last_name": "Smith", "balance": 0},
    {"_id": 4356, "first_name": "Jane", "last_name": "Doe", "balance": 0},
    {"_id": 8734, "first_name": "Mark", "last_name": "Winters", "balance": 0},
    {"_id": 5431, "first_name": "Mary", "last_name": "Brow", "balance": 0},
    {"_id": 3467, "first_name": "Frank", "last_name": "Adams", "balance": 20}
])

# Populate Buildings
buildings = db.buildings
buildings.insert_many([
    {'_id': 134, 'building_name': "Florence"},
    {'_id': 256, 'building_name': "Torrence"}
])

# Populate Rooms
buildings = db.buildings
rooms = db.rooms
florence = buildings.find_one({"building_name": "Florence"})
torrence = buildings.find_one({"building_name": "Torrence"})
rooms.insert_many([
    {'_id': 678, 'room_number': 12, 'building_name': DBRef("buildings", florence["_id"])},
    {'_id': 562, 'room_number': 14, 'building_name': DBRef("buildings", florence["_id"])},
    {'_id': 784, 'room_number': 16, 'building_name': DBRef("buildings", florence["_id"])},
    {'_id': 475, 'room_number': 13, 'building_name': DBRef("buildings", torrence["_id"])},
    {'_id': 963, 'room_number': 23, 'building_name': DBRef("buildings", torrence["_id"])},
    {'_id': 778, 'room_number': 67, 'building_name': DBRef("buildings", torrence["_id"])}
])
# Populate doors
buildings = db.buildings
doors = db.doors
rooms = db.rooms.find()
for i in rooms:
    doors.insert_one({'door_name': 'north',
                      'room_id': DBRef("rooms", i["_id"])})
    doors.insert_one({'door_name': 'west',
                      'room_number': DBRef("rooms", i["_id"])})

# Populate hooks
hooks = db.hooks
hooks.insert_many([
    {'_id': 16745},
    {'_id': 56234},
    {'_id': 47896},
    {'_id': 63748},
    {'_id': 36789}
])

# Populate requests
requests = db.requests
employees = db.employees.find()
rooms = db.rooms.find()

for i in employees:
    for j in rooms:
        requests.insert_one({
            "employee_id": DBRef('employees', i["_id"]),
            "room_number": DBRef('rooms', j["_id"]),
            "date_requested": datetime.now()
        })

# Populate keys
keys = db.keys
hooks = list(db.hooks.find())
doors = list(db.doors.find())

# Starter Keys, some doors don't open
# Fix in later version
keys.insert_many([
    {'_id': 4567,
     'hook_id': DBRef('hooks', hooks[0]['_id']),
     'door_id': DBRef('doors', doors[0]['_id'])},
    {'_id': 7351,
     'hook_id': DBRef('hooks', hooks[0]['_id']),
     'door_id': DBRef('doors', doors[1]['_id'])},
    {'_id': 6542,
     'hook_id': DBRef('hooks', hooks[0]['_id']),
     'door_id': DBRef('doors', doors[3]['_id'])},
    {'_id': 7486,
     'hook_id': DBRef('hooks', hooks[1]['_id']),
     'door_id': DBRef('doors', doors[0]['_id'])},
    {'_id': 2256,
     'hook_id': DBRef('hooks', hooks[2]['_id']),
     'door_id': DBRef('doors', doors[0]['_id'])},
    {'_id': 7652,
     'hook_id': DBRef('hooks', hooks[2]['_id']),
     'door_id': DBRef('doors', doors[4]['_id'])}
])

# Populate Issued_Keys
issued_keys = db.issued_keys
requests = list(db.requests.find())
keys = list(db.keys.find())
today = datetime.now()

issued_keys.insert_many([
    {'request_id': DBRef('requests', requests[0]['_id']),
     'key_id': DBRef('keys', keys[0]['_id']),
     'date_due_back': today.replace(year= today.year + 1),
     'date_returned': None,
     'date_lost': None},
    {'request_id': DBRef('requests', requests[2]['_id']),
     'key_id': DBRef('keys', keys[5]['_id']),
     'date_due_back': today.replace(year= today.year + 1),
     'date_returned': None,
     'date_lost': None},
    {'request_id': DBRef('requests', requests[3]['_id']),
     'key_id': DBRef('keys', keys[0]['_id']),
     'date_due_back': today.replace(year= today.year + 1),
     'date_returned': None,
     'date_lost': None}
])


db.command('collMod', 'employees', **Validators.employees_validator)
db.command('collMod', 'requests', **Validators.requests_validator)
db.command('collMod', 'rooms', **Validators.rooms_validator)
db.command('collMod', 'buildings', **Validators.buildings_validator)
db.command('collMod', 'doors', **Validators.doors_validator)
db.command('collMod', 'hooks', **Validators.hooks_validator)
db.command('collMod', 'keys', **Validators.keys_validator)
db.command('collMod', 'issued_keys', **Validators.issued_keys_validator)