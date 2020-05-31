from alertmgmt.configuration import *
from pymongo import MongoClient
import datetime


# get data between 2 index
def getAllServerData():
    con = MongoClient(MONGO_URL, MONGO_PORT)
    db = con[MONGO_DB][MONGO_COLLECTION_SERVER_DATA]
    cur = db.find({}).sort("createdon", -1)
    d = list(cur)
    cur.close()
    con.close()
    return d


def getServerData(servername):
    con = MongoClient(MONGO_URL, MONGO_PORT)
    db = con[MONGO_DB][MONGO_COLLECTION_SERVER_DATA]
    cur = db.find({'server_name': servername})
    d = list(cur)
    cur.close()
    con.close()
    return d


def insertServerData(server_name, logsource, createdby):
    con = MongoClient(MONGO_URL, MONGO_PORT)
    db = con[MONGO_DB][MONGO_COLLECTION_SERVER_DATA]
    db.insert_one({
        'server_name': server_name,
        'logsource': logsource,
        'createdby': createdby,
        'createdon': datetime.datetime.now()
    });

    con.close()


def deleteServerData(server_name):
    con = MongoClient(MONGO_URL, MONGO_PORT)
    db = con[MONGO_DB][MONGO_COLLECTION_SERVER_DATA]
    db.remove({
        'server_name': server_name
    })

    con.close()


# if __name__ == '__main__':
# #     getAllServerData()
#     insertServerData(
#         'server-loc',
#         '/var/log/message.log',
#         'Subha', datetime.datetime.now()
#     )
