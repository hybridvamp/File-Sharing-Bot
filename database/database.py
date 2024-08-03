#(©)dramaost

import pymongo, os
from config import DB_URI, DB_NAME


dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]

mydb = dbclient["batch_files"]
user_data = database['users']

async def save_batch(string, Name):
    mycol = mydb["batches"]

    data = {
        'string': str(string),
        'name': str(Name)
    }

    try:
        mycol.update_one({'string': str(string)}, {"$set": data}, upsert=True)
    except:
        logger.exception('Some error occured!', exc_info=True)

async def get_batch(string):
    mycol = mydb["batches"]

    try:
        result = mycol.find_one({'string': str(string)})
        if result:
            return result['name']
        else:
            return None
    except:
        logger.exception('Some error occured!', exc_info=True)
        return None

async def get_all_batch():
    mycol = mydb["batches"]

    try:
        result = mycol.find({}, {'string': 1, '_id': 0})
        return [doc['string'] for doc in result]
    except:
        logger.exception('Some error occured!', exc_info=True)
        return []

async def rem_batch(string):
    mycol = mydb["batches"]

    try:
        mycol.delete_one({'string': str(string)})
    except:
        logger.exception('Some error occured!', exc_info=True)

async def get_batch_with_name(name):
    mycol = mydb["batches"]

    try:
        regex = {"$regex": name, "$options": "i"}
        result = mycol.find({"name": regex})
        return [doc['string'] for doc in result]
    except:
        logger.exception('Some error occured!', exc_info=True)
        return False

async def clear_all_batches():
    mycol = mydb["batches"]

    try:
        mycol.delete_many({})
    except:
        logger.exception('Some error occured!', exc_info=True)

async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
        
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return
