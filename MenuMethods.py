import random
from datetime import datetime

from bson import DBRef


def create_key(db):
    # Check if non-empty
    if db.hooks.find() > 0:
        print("There are no hooks, whoops!")
        return

    hooks = db.hooks
    print("valid hooks to choose from:")
    for i in hooks.find():
        print(i["_id"])

    selection = int(input("Enter hook to select: "))

    # Get the hook
    new_hook = db.hooks.find_one({'_id': selection})

    if db.doors.find().count() == 0:
        print("No doors exist to link that hook to, please construct some")
        return
    # now make the door
    doors_list = list(db.doors.find())

    try:
        db.keys.insert_one({'_id': random.randint(3, 999),
                         'hook_id': DBRef('hooks', new_hook['_id']),
                         'door_id': DBRef('doors', doors_list[random.randint(0, len(doors_list) - 1)]['_id'])})
    except Exception as ex:
        print('Could not create key. please check everything is entered correctly')
        return
def list_employee_room_access(db):
    employees = db.employees
    print("Employees:")
    emp_cursor = employees.find()
    for i in emp_cursor:
        print(i["_id"], ": ", i["first_name"], " ", i["last_name"])
    emp = input("Enter the ID of the employee who's access you want to check")
    matching_requests = db.requests.find({"employee_id": {'$ref': 'employees', '$id': emp}})
    # db.requests.find({'employee_id': {'$ref': 'employees', '$id': emp}})
    # Find issued keys based on matching requests
    tmp = []
    for i in matching_requests:
        tmp.append(i["_id"])
    if (len(tmp) == 0):
        print("No keys have been issued for this employee")
        return
    matching_issued_keys = db.issued_keys.find({"request_id": {'$ref': 'requests', '$id': {'$in': tmp}}})

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
        hooks.append(i["hook_id.$id"])
    matching_doors = db.keys.find({"hook_id": {'$ref': 'hooks', '$id': {"$in": hooks}}})

    # Get the door and the room
    cooler_doors = []
    for i in matching_doors:
        cooler_doors.append(i["door_id.$id"])
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
    #matching_issued_keys = list(db.issued_keys.find({"key_id": key}))
    matching_issued_keys = db.issued_keys.find({"request_id": {'$ref': 'requests', '$id': key}})
    try:
      request_ids = []
      for i in matching_issued_keys:
          request_ids.append(i['request_id.$id'])
      # Remove requests associated with those keys
      db.requests.delete_many({'_id' : {'$in': request_ids}})
      # Remove issued keys
      db.issued_keys.delete_many({'key_id': {'$ref': 'keys', '$id': key}})
      # Remove the key
      db.keys.delete_one({'_id': key})
    except Exception as ex:
        return

def lost_key_logged(db):
    # Find issued keys based on matching requests
    lost_key = int(input("Enter the key_id for the lost key: "))
    bad_emp = int(input("Enter your employee id: "))
    # Find employee request
    bad_emp_requests = list(db.requests.find({'employee_id': {'$ref': 'employees', '$id': bad_emp}}))
    if len(bad_emp_requests) == 0:
        print("Please double check that id")
        return
    useable_request = []
    for i in bad_emp_requests:
        useable_request.append(i["_id"])
    # Find the issued key matching the request and key
    try:
        db.issued_keys.update_one({"request_id": {'$ref': 'requests', '$id': {"$in": useable_request}}, "key_id": {'$ref': 'keys', '$id': lost_key}}, {'date_lost': datetime.datetime.now()})
        print("key has been marked as lost, charging employee...")
    except Exception as ex:
        print("Could not resolve update")
    current_emp_bal = list(db.employees.find({'_id': bad_emp}))
    db.employees.update_one({'_id': bad_emp}, {'balance': current_emp_bal[0]['balance'] + 20})

def delete_employee(db):
    #Check to see if employee is there
    employees = db.employees.find()
    print("Employees:")
    try:
        for i in employees:
            print(i["_id"], ": ",  i["first_name"],  " ", i["last_name"])
    except Exception as ex:
        print('could not find employees')
    selection = int(input("Enter the id of the employee you want to delete: "))

    try:
        # Check for outgoing requests
        req = db.requests.find({'employee_id': {'$ref': 'employees', '$id': selection}})
        if req.count() != 0:
            correlating_requests = []
            for i in req:
                correlating_requests.append(i['_id'])
            db.issued_keys.delete_many({'request_id' : {'$ref': 'requests', '$id': {'$in':correlating_requests}}})
            db.requests.delete_many({'employee_id': {'$ref': 'employees', '$id': selection}})
        db.employees.delete_one({'_id': selection})
        print('Employee has been removed')
    except Exception as ex:
        print('Issue locating employee and their requests, please try again')
        return
def add_door(db):
    hooks = db.hooks.find()
    if hooks.count() == 0:
        print('No hooks were found, please try again')
        return
    for i in hooks:
        print('Hook: ', i['_id'])
    chosen_hook = int(input("Enter the hook id you wish to associate the door with: "))

    hook_validation = list(db.hooks.find({'_id': chosen_hook}))
    if len(hook_validation) == 0:
        print('Please check you entered that correctly, we could not locate that hook')
        return
    rooms = db.rooms.find()
    if rooms.count() == 0:
        print('No avaliable options, we cannot find any buildings or rooms')
        return
    print()
    for i in rooms:
        print('Building code: ', i['building_name'], '; room number: ', i['room_number'], '; room id: ', i['id'])
    chosen_room = int(input("> "))

    room_validation = list(db.rooms.find({'id': chosen_room}))
    if len(room_validation) == 0:
        print('Please double check that id, we couldnt find that room')
        return

    print("select a door to choose from")
    door_name = input("> ")

    try:
        results = db.doors.insert_one({
        'door_name': door_name,
        'room_number': DBRef('rooms', room_validation[0]['_id'])
        })
        db.keys.insert_one({ 'hook_id': DBRef('hooks', hook_validation[0]['_id']), 'door_id': DBRef('doors', results.inserted_id)})
        print('Door has been added and a key has been created to open it')
    except Exception as ex:
        print('Error adding, please ensure all params are correct')

def update_request(db):
    employees = db.employees
    requests = db.requests
    rooms = db.rooms
    # Prompt old employee
    old_id = int(input('Enter the id of the employee whos request you want to change'))
    # Locate old requests
    try:
        old_requests = requests.find({'employee_id': {'$ref': 'employees', '$id': old_id}})
        # Get rooms
        request_rooms = []
        for i in old_requests:
            request_rooms.append(i['room_number.$id'])
        requested_rooms = rooms.find({'_id': {'$in': request_rooms}})
    except Exception as ex:
        print("Could not locate employee")
        return
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
        selected_request = requests.update_one({'employee_id': {'$ref': 'employees', '$id': old_id},
                                                'room_number': {'$ref': 'rooms', '$id': selected_room}},
                                               {'$set': {'employee_id': DBRef('employees', new_id)}})
    except Exception as ex:
        print('Error updating, check to make sure the employee id is valid')

def create_request(db):
    employees = db.employees
    buildings = db.buildings
    rooms = db.rooms

    # Collect employee id
    cursor = employees.find()
    try:
        for i in cursor:
            print(i['first_name'] + " " + i['last_name'] + ", id: " + i['_id'])
        emp_id = int(input("Enter your employee id: "))
    except Exception as ex:
        print('Please hire some staff')
        return

    if employees.find_one({'_id': emp_id}).count() == 0:
        print('Invalid id')
        return

    print('Which building do you need access in?\nOptions:')
    try:
        build = buildings.find()
        for i in build:
            print(i['building_name'])
        building_name = input("> ")
    except Exception as ex:
        print("No buildings exist, whoops")
        return

    try:
        building = buildings.find({'building_name': building_name})
        tmp = []
        for i in building:
            tmp.append(i['_id'])
    except Exception as ex:
        print('Could not find that building, please try again')
        return

    try:
        print("Enter the room number you would like to create a request for\nAvailable rooms")
        selected_rooms = rooms.find({'building_name': {'$ref': 'buildings', '$id': {'$in': tmp}}})
        for i in selected_rooms:
            print(i['_id'])
        selected_room_numb = input("> ")
    except Exception as ex:
        print("That building has no rooms!")
        return

    try:
        employee_cursor = employees.find_one({'_id': emp_id})
        room_cursor = rooms.find_one({'_id': selected_room_numb, 'building_name': {'$ref': 'buildings', '$id': tmp[0]}})

        # Each for will only run once! manifesting
        for i in employee_cursor:
            for j in room_cursor:
                db.requests.insert_one({
                    'employee_id': DBRef('employees', i['_id']),
                    'room_number': DBRef('rooms', j['_id']),
                    'date_requested': datetime.now()
                })
        print('Request has been made! Good luck')
    except Exception as ex:
        print("Something went wrong creating your request, please check everything was entered correctly")
        return

def list_room_access(db):
    # Prompt for rooms
    if db.rooms.find().count() == 0:
        print("no rooms exist, please construct some")
        return
    rooms_cursor = db.rooms.find()
    for i in rooms_cursor:
        print("building code: " + i['building_name'] + " room: " + i['room_number'] + " room code: ")
    room_code_selection = int(input("Enter the room code for the room you want access to: "))

    # Find doors associated with room
    doors_as = db.doors.find({'building_name': {'$ref': 'buildings', '$id': room_code_selection}})
    if doors_as.count() == 0:
        print("That room has no doors, please create some")
        return
    # Find Keys asociated with doors
    door_ids = []
    for i in doors_as:
        i.append(i['_id'])
    keys_as = db.keys.find({'door_id': {'$ref': 'doors', '$id': {'$in': door_ids}}})

    if keys_as.count() == 0:
        print('No keys exist for that room, no one can get in')
        return
    # Find Issued_keys associated with keys
    key_ids = []
    for i in keys_as:
        key_ids.append(i['_id'])
    ik_as = db.issued_keys.find({'key_id': {'$ref': 'keys', '$id': {'$in': key_ids}}})

    if ik_as.count() == 0:
        print("No keys have been issued, no employees can enter the room")
        return

    # Find employee requests associated with issued keys
    ik_ids = []
    for i in ik_as:
        ik_ids.append(i['request_id.$id'])

    requests_cursor = db.requests.find({'_id': {'$in': ik_ids}})
    emp_ids = []
    for i in requests_cursor:
        emp_ids.append(i['employee_id.$id'])
    employees_with_access = db.employees.find({'_id': {'$in': emp_ids}})

    no_dupes = []
    print("Employees with access are as follows:")
    for i in employees_with_access:
        if i['_id'] in no_dupes:
            no_dupes.append(i['_id'])
            print(i['first_name'] + " " + i['last_name'])
