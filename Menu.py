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
  elif option == 2:

  # Get employee room access
  elif option == 3:
    MenuMethods.list_employee_room_access(db)

  # Delete a key
  elif option == 4:

  # Delete employee
  elif option == 5:

  # Add new door
  elif option == 6:

  # Change request
  elif option == 7:

  # Log Lost Key
  elif option == 8:

  # Log Room Access
  elif option == 9:

  # exit condition
  elif option == 0:
    return 1
  else:
    print("Something went wrong parsing!")
    return 2