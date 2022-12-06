import random
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

    # Is it valid? TODO

    # Create key
    # Generate new key number
    new_key_number = random.randint(1, 999999)
    # Door for key to open


def list_employee_room_access(db):
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