import subprocess, uuid
from alertmgmt.configuration import *
from pymongo import MongoClient
import datetime


def getMyAssignments(curUser):
    con = MongoClient(MONGO_URL, MONGO_PORT)
    db = con[MONGO_DB][MONGO_COLLECTION]
    cur = db.distinct("assignment_name", {"assignto": curUser})
    d = list(cur)
    res = []
    for aname in d:
        cur = db.find({"assignment_name": aname}).limit(1)
        for c in cur:
            res.append({
                "assignment_name": c['assignment_name'],
                "assignee": c['assignee'],
                "ackstatus": c['ackstatus']
            })


    con.close()
    return res


def getAssignmentTo(curUser):
    con = MongoClient(MONGO_URL, MONGO_PORT)
    db = con[MONGO_DB][MONGO_COLLECTION]
    cur = db.distinct("assignment_name", {"assignee": curUser})
    d = list(cur)
    res = []
    for aname in d:
        cur = db.find({"assignment_name": aname}).limit(1)
        for c in cur:
            res.append({
                "assignment_name": c['assignment_name'],
                "assignto": c['assignto'],
                "ackstatus": c['ackstatus']
            })
    return res


def changeAckFlag(assignment_name):
    con = MongoClient(MONGO_URL, MONGO_PORT)
    db = con[MONGO_DB][MONGO_COLLECTION]
    cur = db.find({"assignment_name": assignment_name}).limit(1)
    tmp = list(cur)[0]
    status = False
    if not tmp['ackstatus']:
        status = True

    db.update_many({'assignment_name': assignment_name}, {'$set':{'ackstatus': status }})

    con.close()


def getLogData(assignment_name):
    con = MongoClient(MONGO_URL, MONGO_PORT)
    db = con[MONGO_DB][MONGO_COLLECTION]
    cur = db.find({"assignment_name": assignment_name})
    res = list(cur)
    con.close()
    return res


def delCompleteAssignment(assignment_name):
    con = MongoClient(MONGO_URL, MONGO_PORT)
    db = con[MONGO_DB][MONGO_COLLECTION]
    db.update_many({'assignment_name': assignment_name}, {'$set': {
        "assignment_name": '',
        "assignee": '',
        "assignto": '',
        "ackstatus": ''
    }})

    con.close()


def getAssignedToName(assignment_name):
    con = MongoClient(MONGO_URL, MONGO_PORT)
    db = con[MONGO_DB][MONGO_COLLECTION]
    cur = db.find({
        "assignment_name": assignment_name
    }).limit(1)
    d = list(cur)[0]
    return d['assignto']


def updateCompleteAssignment(assignment_name, assignee, assignto):
    con = MongoClient(MONGO_URL, MONGO_PORT)
    db = con[MONGO_DB][MONGO_COLLECTION]
    db.update_many({'assignment_name': assignment_name}, {'$set': {
        "assignment_name": assignment_name,
        "assignee": assignee,
        "assignto": assignto,
        "ackstatus": False
    }})

    con.close()


# if __name__ == '__main__':
#     getAssignedToName("tmp-01")
#     changeAckFlag("Assignment-03(2020-05-06 15:44:48.275877)")
    # getAssignmentTo("subha")
    # getMyAssignments("pori")