import pyrebase
from config.firebase_config import firebase_config


class FirebaseDAO:
    def __init__(self, collection):
        firebase = pyrebase.initialize_app(firebase_config)
        self.db = firebase.database()
        self.collection = collection
