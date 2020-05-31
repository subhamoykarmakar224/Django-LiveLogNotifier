import subprocess, uuid
from alertmgmt.configuration import *
from pymongo import MongoClient
import alertmgmt.configuration as cfg
import datetime


# get data between 2 index
def getLogDate(startIndex, endindex):
    con = MongoClient(MONGO_URL, MONGO_PORT)
    db = con[MONGO_DB][MONGO_COLLECTION]
    cur = db.find({"log_seq_index": {"$gte": startIndex, "$lte": endindex}}).sort("log_seq_index", -1)
    d = list(cur)
    cur.close()
    con.close()
    return d


def getSingleLogDate(log_seq_index):
    con = MongoClient(MONGO_URL, MONGO_PORT)
    db = con[MONGO_DB][MONGO_COLLECTION]
    cur = db.find({"log_seq_index": int(log_seq_index)})
    d = list(cur)
    cur.close()
    con.close()
    return d


def updateLogDataComment(log_seq_index, comment):
    con = MongoClient(MONGO_URL, MONGO_PORT)
    db = con[MONGO_DB][MONGO_COLLECTION]
    i = db.update({"log_seq_index": int(log_seq_index)}, {'$set': {"comments": str(comment)}})
    con.close()


def getLastLogSeqIndex():
    lastIndex = 0
    con = MongoClient(MONGO_URL, MONGO_PORT)
    db = con[MONGO_DB][MONGO_COLLECTION]
    cur = db.find({}).sort("log_seq_index", -1).limit(1)
    if cur.count() != 0:
        lastIndex = cur[0]["log_seq_index"]

    cur.close()
    con.close()
    return lastIndex


def getLogDateAsPerSeverityKey(severity_key, sort_engine, date_time_engine, logsource, pageNo):
    start_date_filter = datetime.datetime.strptime(date_time_engine[0], "%B %d, %Y").strftime('%Y-%m-%d')
    start_time_filter = datetime.datetime.strptime(date_time_engine[1], "%I:%M %p").strftime('%H:%M:%S') # 08:30 PM %I:%M %p => 20:30:23 %H:%M:%S
    end_date_filter = datetime.datetime.strptime(date_time_engine[2], "%B %d, %Y").strftime('%Y-%m-%d')
    end_time_filter = datetime.datetime.strptime(date_time_engine[3], "%I:%M %p").strftime('%H:%M:%S')
    con = MongoClient(MONGO_URL, MONGO_PORT)
    db = con[MONGO_DB][MONGO_COLLECTION]
    start_date_time_filter = datetime.datetime.strptime(start_date_filter + " " + start_time_filter, "%Y-%m-%d %H:%M:%S")
    end_date_time_filter = datetime.datetime.strptime(end_date_filter + " " + end_time_filter, "%Y-%m-%d %H:%M:%S")

    severity_name = cfg.SEVERITY_LEVELS[str(severity_key)]
    if logsource == 'all':
        cur = db.find({
            "alarm_type": severity_name,
            "datetimestamp": {'$gte': start_date_time_filter, '$lte': end_date_time_filter},
        }).sort(sort_engine).skip(50 * int(pageNo-1)).limit(50)
    else:
        cur = db.find({
            "alarm_type": severity_name,
            "datetimestamp": {'$gte': start_date_time_filter, '$lte': end_date_time_filter},
            "logsource": logsource
        }).sort(sort_engine).skip(50 * int(pageNo - 1)).limit(50)

    d = list(cur)
    cur.close()
    con.close()
    return d


def getLogDateAsPerTimeStamp(sort_engine, date_time_engine, logsource, pageNo):
    # [('log_seq_index', -1), ('datestamp', -1), ('timestamp', -1)] ['May 03, 2020', '02:35 PM', 'May 04, 2020', '11:27 AM'] 2
    start_date_filter = datetime.datetime.strptime(date_time_engine[0], "%B %d, %Y").strftime('%Y-%m-%d')
    start_time_filter = datetime.datetime.strptime(date_time_engine[1], "%I:%M %p").strftime('%H:%M:%S')  # 08:30 PM %I:%M %p => 20:30:23 %H:%M:%S
    end_date_filter = datetime.datetime.strptime(date_time_engine[2], "%B %d, %Y").strftime('%Y-%m-%d')
    end_time_filter = datetime.datetime.strptime(date_time_engine[3], "%I:%M %p").strftime('%H:%M:%S')

    con = MongoClient(MONGO_URL, MONGO_PORT)
    db = con[MONGO_DB][MONGO_COLLECTION]

    start_date_time_filter = datetime.datetime.strptime(start_date_filter + " " + start_time_filter, "%Y-%m-%d %H:%M:%S")
    end_date_time_filter = datetime.datetime.strptime(end_date_filter + " " + end_time_filter, "%Y-%m-%d %H:%M:%S")

    if logsource == 'all':
        cur = db.find({
            "datetimestamp": {'$gte': start_date_time_filter, '$lte': end_date_time_filter},
        }).sort(sort_engine).skip(50 * int(pageNo-1)).limit(50)
    else:
        cur = db.find({
            "datetimestamp": {'$gte': start_date_time_filter, '$lte': end_date_time_filter},
            "logsource": logsource
        }).sort(sort_engine).skip(50 * int(pageNo - 1)).limit(50)

    d = list(cur)
    cur.close()
    con.close()
    return d


def getFirstAndLastData():
    firstAndLast = {"first": '', "last": ''}
    con = MongoClient(MONGO_URL, MONGO_PORT)
    db = con[MONGO_DB][MONGO_COLLECTION]
    cur = db.find({}).sort('log_seq_index', -1).limit(1)
    if cur.count() != 0:
        firstAndLast["last"] = list(cur)[0]
    else:
        firstAndLast["last"] = 0

    cur = db.find({}).sort('log_seq_index', 1).limit(1)

    if cur.count() != 0:
        firstAndLast["first"] = list(cur)[0]
    else:
        firstAndLast["first"] = 0

    cur.close()
    con.close()
    return firstAndLast


def getGroupedCount():
    severity_group_count = {}
    for k in cfg.SEVERITY_LEVELS.keys():
        if cfg.SEVERITY_LEVELS[k] != 'None':
            severity_group_count[cfg.SEVERITY_LEVELS[k]] = 0

    con = MongoClient(MONGO_URL, MONGO_PORT)
    db = con[MONGO_DB][MONGO_COLLECTION]
    cur = db.aggregate([{"$group": {'_id': "$alarm_type", "count": {"$sum": 1}}}])
    for c in cur:
        field = c['_id']
        cnt = int(c['count'])
        severity_group_count[field] = cnt

    cur.close()
    con.close()
    return severity_group_count


def getGroupedCountFiltered(severity_level_filter, date_time_engine, logsource):
    # 08:30 PM %I:%M %p => 20:30:23 %H:%M:%S
    start_date_filter = datetime.datetime.strptime(date_time_engine[0], "%B %d, %Y").strftime('%Y-%m-%d')
    start_time_filter = datetime.datetime.strptime(date_time_engine[1], "%I:%M %p").strftime('%H:%M:%S')
    end_date_filter = datetime.datetime.strptime(date_time_engine[2], "%B %d, %Y").strftime('%Y-%m-%d')
    end_time_filter = datetime.datetime.strptime(date_time_engine[3], "%I:%M %p").strftime('%H:%M:%S')

    start_date_time_filter = datetime.datetime.strptime(start_date_filter + " " + start_time_filter,"%Y-%m-%d %H:%M:%S")
    end_date_time_filter = datetime.datetime.strptime(end_date_filter + " " + end_time_filter, "%Y-%m-%d %H:%M:%S")

    severity_group_count = {}
    for k in cfg.SEVERITY_LEVELS.keys():
        if cfg.SEVERITY_LEVELS[k] != 'None':
            severity_group_count[cfg.SEVERITY_LEVELS[k]] = 0

    con = MongoClient(MONGO_URL, MONGO_PORT)
    db = con[MONGO_DB][MONGO_COLLECTION]

    if str(severity_level_filter) == '-1':
        if logsource == 'all':
            cur = db.aggregate([
                {"$match": {"datetimestamp": {'$gte': start_date_time_filter, '$lte': end_date_time_filter}}},
                {"$group": {'_id': "$alarm_type", "count": {"$sum": 1}}}
            ])
        else:
            cur = db.aggregate([
                {"$match": {"datetimestamp": {'$gte': start_date_time_filter, '$lte': end_date_time_filter}, "logsource": logsource}},
                {"$group": {'_id': "$alarm_type", "count": {"$sum": 1}}}
            ])
    else:
        if logsource == 'all':
            cur = db.aggregate([
                {"$match": {"alarm_type": cfg.SEVERITY_LEVELS[severity_level_filter], "datetimestamp": {'$gte': start_date_time_filter, '$lte': end_date_time_filter}}},
                {"$group": {'_id': "$alarm_type", "count": {"$sum": 1}}}
            ])
        else:
            cur = db.aggregate([
                {"$match": {"alarm_type": cfg.SEVERITY_LEVELS[severity_level_filter],
                            "datetimestamp": {'$gte': start_date_time_filter, '$lte': end_date_time_filter}, "logsource": logsource}},
                {"$group": {'_id': "$alarm_type", "count": {"$sum": 1}}}
            ])

    for c in cur:
        field = c['_id']
        cnt = int(c['count'])
        severity_group_count[field] = cnt

    cur.close()
    con.close()
    return severity_group_count


def getUniqueServerLocations():
    logsourcelist = []
    con = MongoClient(cfg.MONGO_URL, cfg.MONGO_PORT)
    db = con[cfg.MONGO_DB][cfg.MONGO_COLLECTION_SERVER_DATA]
    cur = db.distinct("server_name")
    for c in cur:
        logsourcelist.append(str(c))
    con.close()
    return logsourcelist


def getServerURL(servername):
    con = MongoClient(cfg.MONGO_URL, cfg.MONGO_PORT)
    db = con[cfg.MONGO_DB][cfg.MONGO_COLLECTION_SERVER_DATA]
    cur = db.find({"server_name": servername})
    d = ''
    try:
        d = list(cur)[0]['logsource']
    except:
        return 'all'
    con.close()
    return d


def addNewAssignments(assignment_name, assignee, ackstatus, loglist, assignto):
    con = MongoClient(cfg.MONGO_URL, cfg.MONGO_PORT)
    db = con[cfg.MONGO_DB][cfg.MONGO_COLLECTION]
    loglist = loglist[:len(loglist)-4]
    loglist = loglist.split(" _;_ ")
    timeStamp = str(datetime.datetime.now())
    data = []
    for l in loglist:
        tmpCnt = l[:l.index("-")].strip(" ")
        tmpAlertID = l[l.index("-")+1:].strip(" ")
        tmpData = {
            "assignment_name": assignment_name + "(" + timeStamp + ")",
            "assignee": assignee,
            "assignto": assignto,
            "ackstatus": ackstatus
        }

        db.update(
            {
                "alert_id": str(tmpAlertID),
                "log_seq_index": int(tmpCnt),
            },
            {'$set': tmpData}
        )

    con.close()
