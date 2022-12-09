from pymongo import MongoClient
import Menu

# Mongo setup
cluster = "mongodb+srv://kupo:001657916579@termproject.7grkfgp.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(cluster)
db = client.Term_Project

# menu loop
print("Welcome!")
active_menu = True
while active_menu:
    val = Menu.io_Menu(db)
    if val is 1:
        active_menu = False
    # catch any weird errors
    if val is 2:
        print("Wtf, this is redundant, how did you get here?")
        active_menu = False
print("Thank you!")