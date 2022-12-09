import random
from datetime import datetime

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
        except Exeption as ex:
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
    if (len(tmp) == 0):
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
    try:
      request_ids = []
      for i in matching_issued_keys:
          request_ids.append(i['request_id'])
      # Remove requests associated with those keys
      db.requests.delete_many({'_id' : {'$in': request_ids}})
      # Remove issued keys
      db.issued_keys.delete_many({'key_id': key})
      # Remove the key
      db.keys.delete_one({'_id': key})
    except Exception return as ex:
      return

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

def delete_employee(db):
  #Check to see if employee is there
  employees = db.employees
    print("Employees:")
  try:
    for i in employees:
        print(i["_id"]+": " + i["first_name"] + " " + i["last_name"])
    emp = input("Enter the ID of the employee who's access you want to check")
    matching_requests = db.employees.find({"employee_id": emp })
    
  employee_id = int(input("Enter the employee_id: "))
  
    matching_requests = db.requests.find({"employee_id": emp })
  #Once the employee(s) with the matching ids have been found delte them
  try:
      request_ids = []
      for i in matching_requests:
          request_ids.append(i['request_id'])
      # Remove requests associated with those employee
      db.requests.delete_many({'_id' : {'$in': request_ids}})
      # Remove the employee
      db.employees.delete_one({'_id': employee})
    except Exception return as ex:
      return

def add_door(db):
  # Check if non-empty
    if db.hooks.find().count() > 0:
        print("There are no hooks, whoops!")
        return
    hooks = db.hooks
    print("valid hooks to choose from:")
    for i in hooks.find():
        print(i["_id"])

    selection = int(input("Enter hook to select: "))
  building_name = (input("Enter the name of the building: "))
  room_num = int(input("Enter the room number of said building"))
  key_id = int(input("Enter the key_id for the new door: "))
  new_door = (selection, building_name, room_num, key_id, new_door)
   # now make the door
        doors_list = list(db.doors.find())

        try:
            keys = db.keys
            keys.insert_one({'_id': random.randint(3, 999),
                             'hook_id': DBRef('hooks', new_hook[0]['_id']),
                             'door_id': DBRef('doors', doors_list[random.randint(0, len(doors_list) - 1)]['_id'])})
        except Exeption as ex:
            return
  doors_list.append(new_door)


def update_request(db):
    employees = db.employees
    requests = db.requests
    rooms = db.rooms
    # Prompt old employee
    old_id = int(input('Enter the id of the employee whos request you want to change'))
    # Locate old requests
    old_requests = requests.find({'employee_id': old_id})
    # Get rooms
    request_rooms = []
    for i in old_requests:
        request_rooms.append(i['room_number'])
    requested_rooms = rooms.find({'_id': {'$in': request_rooms}})

    # List room requests
    print('Rooms you can modify are:')
    for i in requested_rooms:
        print(i['_id'])
    # Get room to be updated
    selected_room = int(input('Room number: '))

    # Get new employee number
    new_id = int(input("And the new employee id: "))

    # Update
    try:
        selected_request = requests.update_one({'employee_id': old_id, 'room_number': selected_room},
                                               {'$set': {'employee_id': new_id}})
    except Exception as ex:
        print('Error updating, check to make sure the employee id is valid')


def create_request(db):
    employees = db.employees
    buildings = db.buildings
    rooms = db.rooms

    # Collect employee id
    emp_id = int(input("Enter your employee id: "))
    print('Which building do you need access in?\nOptions:')
    build = buildings.find()
    for i in build:
        print(i['building_name'])
    building_name = input("")

    building = buildings.find({'building_name': building_name})
    tmp = []
    for i in building:
        tmp.append(i['_id'])

    print("Enter the room number you would like to create a request for\nAvailable rooms")
    selected_rooms = buildings.find({'building_name': {'$in': tmp}})
    for i in selected_rooms:
        print(i['_id'])
    selected_room_numb = input("")

    employee_cursor = employees.find_one({'_id': emp_id})
    room_cursor = rooms.find_one({'_id': selected_room_numb, 'building_name': tmp[0]})

    # Each for will only run once! manifesting
    for i in employee_cursor:
        for j in room_cursor:
            db.requests.insert_one({
                'employee_id': DBRef('employees', i['_id']),
                'room_number': DBRef('rooms', j['_id']),
                'date_requested': datetime.now()
            })
    print('Request has been made! Good luck')

def list_room_access(db):
    # Prompt for rooms
    rooms_cursor = db.rooms.find()
    for i in rooms_cursor:
        print("building code: " + i['building_name']+" room: " + i['_id'])
    selected_room = input("Enter the room number")
    # Find doors associated with room
    # Find Keys asociated with doors
    # Find Issued_keys associated with keys
    # Find employee requests associated with issued keys
