from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb://localhost:27017')

db = client.Record

patient_collection = db.patient

#defaul value
try:
    patient_collection.update_many(
        {},
        {
            '$set': {
                'blood_group': 'Unknow',
                'rhesus_factor': 'Unknow'
            }
        } )
except Exception as e:
    print('Error: ', e)

client.close()
