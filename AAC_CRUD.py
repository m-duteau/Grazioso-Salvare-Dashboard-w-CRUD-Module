from pymongo import MongoClient
from bson.objectid import ObjectId


class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections.
        # This is hard-wired to use the aac database, the 
        # animals collection, and the aac user.
        # Definitions of the connection string variables are
        # unique to the individual Apporto environment.
        #
        # Connection Variables
        #
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 30476
        DB = 'AAC'
        COL = 'animals'
        #
        # Initialize Connection
        #
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (username, password, HOST, PORT))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]

# Create method to implement the C in CRUD.
    def create(self, data):
        if data is not None:
            insert_dict = self.database.animals.insert_one(data)  # data should be dictionary
            if insert_dict != 0:  # return true if insert_dict contains data
                return True
            else:  # false otherwise
                return False
        else:
            raise Exception("Nothing to save, because data parameter is empty")

# Method to implement the R in CRUD.
    def read(self, search_data): 
        search_result = []
        if search_data is not None:  # parameter is not empty
            if search_data == "all":
                search_result = self.database.animals.find({})
            else:
                search_result = self.database.animals.find(search_data)  # find search_data in db "animals"     
        else:
            raise Exception("Nothing to read, because data parameter is empty")
        return search_result

# Method to implement the U in CRUD
    def update(self, original_doc, updated_doc):
        if original_doc is not None:
            count = self.database.animals.count_documents(original_doc)
            if count != 0:
                if count == 1:
                    update = self.database.animals.update_one(original_doc, {"$set": updated_doc})
                elif count > 1:
                    update = self.database.animals.update_many(original_doc, {"$set": updated_doc})
                return update.raw_result
            else:
                return "Document not found"
        else:
            raise Exception("Nothing to update, because data parameter is empty")

# Method to implement the D in CRUD
    def delete(self, delete_doc):
        if delete_doc is not None:
            count = self.database.animals.count_documents(delete_doc)
            if count != 0:
                if count == 1:
                    delete = self.database.animals.delete_one(delete_doc)
                elif count > 1:
                    delete = self.database.animals.delete_many(delete_doc)
                return delete.raw_result
            else:
                return "Document not found"
        else:
            raise Exception("Nothing to delete, because data parameter is empty")
