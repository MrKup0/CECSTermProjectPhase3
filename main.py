from Utilities import Utilities
import Menu

db = Utilities.startup()

sizes = db.sizes()
db.insert_many([
        {"name": "small", "diameter": 10},
        {"name": "medium", "diameter": 15},
        {"name": "large", "diameter": 22},
        {"name": "oh wow", "diameter": 36}
])