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
    return 0
  # Create request
  elif option == 2:
    MenuMethods.create_request(db)
    return 0

  # Get employee room access
  elif option == 3:
    MenuMethods.list_employee_room_access(db)
    return 0

  # Delete a key
  elif option == 4:
    MenuMethods.delete_key(db)
    return 0

  # Delete employee
  elif option == 5:
    MenuMethods.delete_employee(db)
    return 0

  # Add new door
  elif option == 6:
    MenuMethods.add_door(db)
    return 0

  # Change request
  elif option == 7:
    MenuMethods.update_request(db)
    return 0

  # Log Lost Key
  elif option == 8:
    MenuMethods.lost_key_logged(db)
    return 0

  # Log Room Access
  elif option == 9:
    MenuMethods.list_room_access(db)
    return 0
  # exit condition
  elif option == 0:
    return 1
  else:
    print("Something went wrong parsing!")
    return 2
