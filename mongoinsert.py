"""Insert data to mongodb."""
import pymongo
import json

# Creating connection to mongo client
connection = pymongo.MongoClient()
# creating a collection name if not exist.
collection = connection.jabong.jabong_data

documents = json.load(open('jabong.json', 'r'))
# print docs
for document in documents:
    collection.save(document)
connection.close()
