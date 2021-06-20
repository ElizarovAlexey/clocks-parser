from pymongo import MongoClient

cluster = MongoClient(
    'mongodb+srv://admin:admin@test.8axby.mongodb.net/Clocks?retryWrites=true&w=majority')

db = cluster['Clocks']
collection = db['RussianClocks']
