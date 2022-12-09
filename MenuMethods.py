import datetime
import random

from bson import DBRef


def create_key(db):
    # Check if non-empty
    if db.hooks.find().count() > 0:
        print("There are no hooks, whoops!")
        return

    hooks = db.hooks
    print("valid hooks to choose from:")
    for i in hooks.find():
        print(i["_id"])

    selection = int(input("Enter hook to select: "))

    try:
        # Get the hook
        new_hook = list(db.hooks.find_one({'_id': selection}))
        # Create key
        # Door for key to open
        # Check there are doors
        if not (db.doors.find().count() > 0):
            print("No doors exist, please construct some")
            return
        # now make the door
        doors_list = list(db.doors.find())

        try:
            keys = db.keys
            keys.insert_one({'_id': random.randint(3, 999),
                             'hook_id': DBRef('hooks', new_hook[0]['_id']),
                             'door_id': DBRef('doors', doors_list[random.randint(0, len(doors_list) - 1)]['_id'])})
        except Exception as ex:
            return

def list_employee_room_access(db):
    employees = db.employees
    print("Employees:")
    for i in employees:
        print(i["_id"]+": " + i["first_name"] + " " + i["last_name"])
    emp = input("Enter the ID of the employee who's access you want to check")
    matching_requests = db.requests.find({"employee_id": emp })

    # Find issued keys based on matching requests
    tmp = []
    for i in matching_requests:
        tmp.append(i["_id"])
    if not (len(tmp) > 0):
        print("No keys have been issued for this employee")
        return
    matching_issued_keys = db.issued_keys.find({"request_id": {"$in": tmp}})

    # Use the key_id to match to parent keys
    keys = []
    for i in matching_issued_keys:
        keys.append(i["key_id"])
    if not (len(keys) > 0):
        print("Uh oh")
        return
    matching_keys = db.keys.find({"_id": {"$in": keys}})

    # Get the hooks associated with those keys
    hooks = []
    for i in matching_keys:
        hooks.append(i["hook_id"])
    matching_doors = db.keys.find({"hook_id": {"$in": hooks}})

    # Get the door and the room
    cooler_doors = []
    for i in matching_doors:
        cooler_doors.append(i["door_id"])
    valid_doors = db.doors.find({'_id': {'$in': cooler_doors}})
    cooler_rooms = []
    for i in valid_doors:
        cooler_rooms.append(i['room_number'])

    access_rooms = db.rooms.find({'_id': {'$in': cooler_rooms}})

    # Return the unique rooms associated with the keys
    print("Employee can open:")
    bar = [] # my poor memory
    for i in access_rooms:
        room = i['_id']
        building = i['building_name']
        pirate = (room, building)
        if pirate not in bar:
          print(room + " in " + building)

def delete_key(db):
    #Check to see if there is a key that is created
    l_keys = list(db.keys.find())
    for i in l_keys:
        print("key_id: "+ i['_id'])
    key = int(input("enter the key_id of the key you wish to remove: "))
    matching_issued_keys = list(db.issued_keys.find({"key_id": key}))
    request_ids = []
    for i in matching_issued_keys:
        request_ids.append(i['request_id'])
    # Remove requests associated with those keys
    db.requests.delete_many({'_id' : {'$in': request_ids}})
    # Remove issued keys
    db.issued_keys.delete_many({'key_id': key})
    # Remove the key
    db.keys.delete_one({'_id': key})


def lost_key_logged(db):
    # Find issued keys based on matching requests
    lost_key = int(input("Enter the key_id for the lost key: "))
    bad_emp = int(input("Enter your employee id: "))
    # Find employee request
    bad_emp_requests = list(db.requests.find({'employee_id': bad_emp}))
    if len(bad_emp_requests) == 0:
        print("Please double check that id")
        return
    useable_request = []
    for i in bad_emp_requests:
        useable_request.append(i["_id"])
    # Find the issued key matching the request and key
    try:
        matching_issued_keys = db.issued_keys.update_one(
            {"request_id": {"$in": useable_request}, "key_id": lost_key},
            {'date_lost': datetime.datetime.now()}
        )
        print("key has been marked as lost, charging employee...")
    except Exception as ex:
        print("Could not resolve update")
    current_emp_bal = list(db.employees.find({'_id': bad_emp}))
    db.employees.update_one({'_id': bad_emp}, {'balance': current_emp_bal[0]['balance'] + 20})