import getpass
import pymongo
from pymongo import MongoClient


class Utilities:
    """I have several variations on a theme in this project, and each one will need to start up
    with the same MongoDB database.  So I'm putting any sort of random little utilities in here
    as I need them.

    startup - creates the connection and returns the database client."""
    @staticmethod
    def startup():
        #print("Prompting for the password.")
        #password = getpass.getpass(prompt='MongoDB password --> ')
        # cluster = "mongodb+srv://CECS_323:" + password + "@cluster0.a5iq9hc.mongodb.net/demo_database?retryWrites=true&w=majority"
        cluster = "mongodb+srv://Kupo:password1234@termproject.7grkfgp.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(cluster)
        # I could also have said "db = client.demo_database" to do the same thing.
        db = client.term_project
        return db

    """Return the size document for the given name."""
    @staticmethod
    def get_size(db, size_name):
        result = db.sizes.find_one({"name": size_name})['_id']
        return result
