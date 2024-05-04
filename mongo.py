import pymongo
import bson


client = pymongo.MongoClient('localhost', 27017)

db = client['RLT_db']
collection  = db['RLT_db']


with open('sampleDB\\sample_collection.bson', 'rb') as f:
    data = bson.decode_all(f.read())

if not collection.count_documents({}):
    collection.insert_many(data)
    