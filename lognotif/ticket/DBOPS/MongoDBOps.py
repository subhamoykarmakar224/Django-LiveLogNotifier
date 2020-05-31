from alertmgmt.configuration import *
from pymongo import MongoClient


def getTickets(username):
    con = MongoClient(MONGO_URL, MONGO_PORT)
    db = con[MONGO_DB][MONGO_COLLECTION_TICKETS]
    cur = db.find({"author": str(username)})
    d = []
    try:
        d = list(cur)
    except:
        cur.close()
        con.close()
        return d
    cur.close()
    con.close()
    return d


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


def getLastTickCnt(user):
    print("AUTHOR :: ", user)
    con = MongoClient(MONGO_URL, MONGO_PORT)
    db = con[MONGO_DB][MONGO_COLLECTION_TICKETS]
    cur = db.find({
        "author": str(user)
    }).sort("timestamp", -1).limit(1)

    try:
        cur = list(cur)[0]
    except:
        return 1

    tmpS = str(cur['ticket_id'])
    cnt = int(tmpS[tmpS.index('TT') + 2:])
    return cnt + 1


def insertTicket(ticket_id, ticket_name, assignment_name, author, timestamp, comments):
    con = MongoClient(MONGO_URL, MONGO_PORT)
    db = con[MONGO_DB][MONGO_COLLECTION_TICKETS]
    db.insert_one({
        'ticket_id': ticket_id,
        'ticket_name': ticket_name,
        'assignment_name': assignment_name,
        'author': author,
        'timestamp': timestamp,
        'comments': comments,
        'status': 1
    })
    con.close()


def deleteTicket(ticketId):
    con = MongoClient(MONGO_URL, MONGO_PORT)
    db = con[MONGO_DB][MONGO_COLLECTION_TICKETS]
    db.delete_one({
        'ticket_id': ticketId
    })
    con.close()


def changeTicketStatus(ticketId):
    con = MongoClient(MONGO_URL, MONGO_PORT)
    db = con[MONGO_DB][MONGO_COLLECTION_TICKETS]
    cur = db.find({'ticket_id': ticketId})
    d = list(cur)[0]
    if d['status'] == 1:
        db.update({'ticket_id': ticketId},
                  {'$set': {"status": 0}}
                  )
    else:
        db.update({'ticket_id': ticketId},
                  {'$set': {"status": 1}}
                  )

    con.close()
