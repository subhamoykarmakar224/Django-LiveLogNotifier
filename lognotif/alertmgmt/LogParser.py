import uuid
from alertmgmt.configuration import *
from pymongo import MongoClient


# Parse Log Line
def parseData(logData, logsource, n):
    logData = logData.decode("utf-8")
    log_data = {'alert_id': str(uuid.uuid4()), 'alarm_name': '', 'alarm_type': '', 'alarm_details': '', 'log_seq_index': '',
                'severity': '', 'color': '', 'facility': '', 'datestamp': '', 'timestamp': '', 'hostname': '', 'app-name': '', 'comments': '',
                'logsource': logsource};
    sev_fac = logData[1:logData.index(')')].split(", ")
    logData = logData[logData.index(") ") + 2:]
    log_data['alarm_type'] = SEVERITY_LEVELS[sev_fac[0]]
    log_data['severity'] = sev_fac[0]
    log_data['color'] = SEVERITY_COLOR_CODE[sev_fac[0]]
    log_data['facility'] = sev_fac[1]
    log_data['datestamp'] = logData[:logData.index(' ')]
    logData = logData[logData.index(" ") + 1:]
    log_data['timestamp'] = logData[:logData.index(' ')]
    logData = logData[logData.index(" ") + 1:]
    log_data['hostname'] = logData[:logData.index(' ')]
    logData = logData[logData.index(" ") + 1:]
    log_data['app-name'] = logData[:logData.index(' ')]
    logData = logData[logData.index(" ") + 1:]
    log_data['alarm_details'] = logData.strip("\n")
    # log_data['log_seq_index'] = getLastLogSeqIndex() + 1
    log_data['log_seq_index'] = n
    insertLogData(log_data)


# Inserts Log Data to DB
def insertLogData(data):
    con = MongoClient(MONGO_URL, MONGO_PORT)
    db = con[MONGO_DB][MONGO_COLLECTION]
    db.insert_one(data)


# Gets the last index of log insert into the database
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

# if __name__ == '__main__':
#     print(getLastLogSeqIndex())