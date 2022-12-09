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
    key = int(input("enter the key_id of the key: "))
    rmp = []
    for i in key:
        rmp.append(i["_id"])
    if not (len(rmp) > 0):
        print("No keys have been issued for this employee")
        return
    matching_issued_keys = db.issued_keys.find({"request_id": {"$in": rmp}})
  #Once all issued keys have been found delete them if they exsist
      if (key in matching_issued_keys):
        del key
    else:
        print("Key does not exsist please try again. ")

def lost_key_logged(db):
    # Find issued keys based on matching requests
    lost_key = int(input("Enter the key_id for the lost key: "))
    tmp = []
    for i in lost_key:
        tmp.append(i["_id"])
    if not (len(tmp) > 0):
        print("No keys have been issued for this employee")
        return
    matching_issued_keys = db.issued_keys.find({"request_id": {"$in": tmp}})
  #Once all keys have been found check if the key logged exsist
    if lost_key in matching_issued_keys:
        print("Key has been recorded")
        return lost_key

    else:
        print("Key does not exsist.")
        return
def delete_employee(db):
  #Check to see if employee is there
  employee_id = int(input("Enter the employee_id: "))
  rmp = []
    for i in employee_id:
        rmp.append(i["_id"])
    if not (len(rmp) > 0):
        print("No id identification have been issued for this employee(s)")
        return
    matching_requests = db.requests.find({"employee_id": rmp })
  #Once the employee(s) with the matching ids have been found delte them
  if employee_id in matching_requests:
    del employee_id
  else:
    print("No employee with said id exsists.")
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
