import MenuMethods
def menu(): # Pres order
  print("[1] Create a new Key") # Jacob
  print("[2] Request Access") # Angel
  print("[3] Check Room Access") # Jacob
  print("[4] Delete a Key") # Angel
  print("[5] Delete Employee") # Jacob
  print("[6] Add new Door") # Angel
  print("[7] Change Request") # Jacob
  print("[8] Lost key") # Angel
  print("[9] Log room access") # Jacob
  print("[0] Quit")

def io_Menu(db):
  menu()
  option = int(input("Enter your choice "))

  # Create new key
  if option == 1:
    MenuMethods.create_key(db)
  # Create request
    def create_key(db):
    # Check if non-empty
    if db.hooks.find().count() > 0:
        print("There are no hooks, whoops!")
        return

    hooks = db.hooks
    print("valid hooks to choose from:")
    for i in hooks:
        print(i["hook_id"])

    selection = int(input("Enter hook to select: "))
    new_hook = hooks

    # Is it valid? TODO

    # Create key
    # Generate new key number
    new_key_number = random.randint(1, 999999)
    # Door for key to open
    # Check there are doors
    if not (db.doors.find().count() > 0):
        print("No doors exist, please construct some")
        return
    # now make the door
    doors = db.doors.find()
    new_door = doors[random.randint(0, doors.count() - 1)]
    final_new_key = {
        "door_name": DBRef("doors", new_door["door_name"]),
        "room_number": DBRef("doors", new_door["room_number"]),
        "building_name": DBRef("doors", new_door["building_number"]),
        "hook_id": selection,
        "key_id": new_key_number
    }

    # does this match the validator?
    try:
        keys = db.keys
        keys.insert_one(final_new_key)

  elif option == 2:

  # Get employee room access
  elif option == 3:
    MenuMethods.list_employee_room_access(db)
    employees = db.employees
    print("Employees:")
    for i in employees:
        print(i["_id"]+": " + i["first_name"] + " " + i["last_name"])
    emp = input("Enter the ID of the employee who's access you want to check")
    matching_requests = db.requests.find({ "employees_id": emp })

    # Find issued keys based on matching requests
    tmp = []
    for i in matching_requests:
        tmp.append(i["_ID"])
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
    matching_keys = db.keys.find({"_ID": {"$in": keys}})

    # Get the hooks associated with those keys
    hooks = []
    for i in matching_keys:
        hooks.append(i["hook_id"])
    matching_doors = db.keys.find({"hook_id": {"$in": hooks}})

    # Return the unique rooms associated with the keys
    print("Employee can open:")
    bar = [] # my poor memory
    for i in matching_doors:
        room = i["room_number"]
        building = i["building_name"]
        pirate = (room, building)
        if pirate not in bar:
            print(room + " in " + building)
            bar.append(pirate)

  # Delete a key
  elif option == 4:
    def delete_key(db):
    #Check to see if there is a key that is created

    if db.hooks.find().count() == 0:
        print("There are no hooks, whoops!")
        return
    #Use the necessary hook_id to find a key put it in a variable then delete it upon return
    key = int(input(: "enter the key_id of the key"))
    if key == key_id:
        key == key_id
    if (key in lost_keys):
        return del key
    elif (key in returned_keys):
        return del key()
    elif (key in issued_keys):
        return del key()
    else:
        print("key not found")
        return

  # Delete employee
  elif option == 5:

  # Add new door
  elif option == 6:
    def add_door(db):
    employees = db.employees
    print("Employees:")
    for i in employees:
        print(i["_id"] + ": " + i["first_name"] + " " + i["last_name"])
    emp = input("Enter the ID of the employee who's access you want to check")
    matching_requests = db.requests.find({"employees_id": emp})
    issued_keys = db.issued_keys
    doors = db.doors.find()
    new_door = doors[random.randint(0, doors.count() - 1)]
    door_number = int(input("Enter the door number: "))
    key_number = int(input("Enter the key number: "))
    if door_number == key_number:
        return new_door
    else:
        print("Current key is not compatiable with new door.")




  # Change request
  elif option == 7:

  # Log Lost Key
  elif option == 8:
    def lost_key_logged(db):
    if db.hooks.find().count() == 0:
        print("There are no hooks, whoops!")
        return
    #print out the employee_id for the one who lost they key
    emp = input("Enter the id of the employee who lost the key: ")
    lost_key = int(input("Enter the key_id for the lost key: " ))
    due_date = input("Enter the due date of when key is supposed to be returned: ")
    if lost_key == issued_keys:
        print("Key has been recorded")
        return emp
        return lost_key
        return due_date
    else:
        print("Key does not exsist.")
        return


  # Log Room Access
  elif option == 9:

  # exit condition
  elif option == 0:
    return 1
  else:
    print("Something went wrong parsing!")
    return 2