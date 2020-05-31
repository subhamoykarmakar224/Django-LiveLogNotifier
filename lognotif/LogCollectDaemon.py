import subprocess
import uuid, threading, datetime
from pymongo import MongoClient
import time


class RunDaemon():
    def __init__(self):
        super(RunDaemon, self).__init__()
        self.thread_stop_flag = True
        self.MONGO_URL = "localhost"
        self.MONGO_PORT = 27017
        self.MONGO_DB = "LogNotifier"
        self.MONGO_COLLECTION = "alert_log"
        self.MONGO_COLLECTION_SERVER_DATA = "server_data"
        self.SEVERITY_LEVELS = {
            '-1': 'None',
            '0': 'Emergency',
            '1': 'Alert',
            '2': 'Critical',
            '3': 'Error',
            '4': 'Warning',
        }

        self.SEVERITY_COLOR_CODE = {
            '0': 'red',
            '1': 'red',
            '2': 'red',
            '3': 'orange',
            '4': 'blue'
        }

    def run(self):
        logsources = self.getUniqueServerLocations()
        threads = []
        cnt = 0
        for src in logsources:
            cnt += 1
            lastValidSeqIndex = self.getLastLogSeqIndex(src)
            con = MongoClient(self.MONGO_URL, self.MONGO_PORT)
            db = con[self.MONGO_DB][self.MONGO_COLLECTION]
            threads.append(
                threading.Thread(target=self.job, name='Thread-' + str(cnt), args=(int(lastValidSeqIndex), db, src, ))
            )

        print("Starting threads...")
        for t in threads:
            t.start()
        print('Joining Threads...')
        for t in threads:
            t.join()

        print("Background log collection daemon started...")

    def job(self, lastValidSeqIndex, db, logsource):
        while self.thread_stop_flag:
            process = subprocess.Popen(["tail", "-f", logsource], stdout=subprocess.PIPE)
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    lastValidSeqIndex = lastValidSeqIndex + 1
                    self.parseData(output.strip(), logsource, lastValidSeqIndex, db)
            rc = process.poll()
            return rc

    # Parse Log Line
    def parseData(self, logData, logsource, n, db):
        logData = logData.decode("utf-8")
        log_data = {'alert_id': str(uuid.uuid4()), 'alarm_name': '', 'alarm_type': '', 'alarm_details': '',
                    'log_seq_index': '', 'severity': '', 'color': '', 'facility': '', 'datestamp': '',
                    'timestamp': '', 'datetimestamp': '', 'hostname': '', 'app-name': '', 'comments': '',
                    'logsource': logsource, 'servername': '', 'assignee': '', 'assignto': '', 'ackstatus': '',
                    'collecttimestamp': '', "assignment-name": '', 'app_name': ''
                    };
        sev_fac = logData[1:logData.index(')')].split(", ")
        logData = logData[logData.index(") ") + 2:]
        try:
            log_data['alarm_type'] = self.SEVERITY_LEVELS[sev_fac[0]]
        except:
            return
        log_data['severity'] = sev_fac[0]
        log_data['color'] = self.SEVERITY_COLOR_CODE[sev_fac[0]]
        log_data['facility'] = sev_fac[1]
        log_data['datestamp'] = logData[:logData.index(' ')]
        logData = logData[logData.index(" ") + 1:]
        log_data['timestamp'] = logData[:logData.index(' ')]
        logData = logData[logData.index(" ") + 1:]
        log_data['hostname'] = logData[:logData.index(' ')]
        logData = logData[logData.index(" ") + 1:]
        log_data['app-name'] = logData[:logData.index(' ')]
        log_data['app_name'] = logData[:logData.index(' ')]
        logData = logData[logData.index(" ") + 1:]
        log_data['alarm_details'] = logData.strip("\n")
        d = datetime.datetime.strptime(log_data['datestamp'] + " " + log_data['timestamp'], "%Y-%m-%d %H:%M:%S")
        log_data['datetimestamp'] = d
        log_data['log_seq_index'] = n
        log_data['collecttimestamp'] = datetime.datetime.now()
        db.insert_one(log_data)

    # Gets the last index of log insert into the database
    def getLastLogSeqIndex(self, logsource):
        lastIndex = 0
        con = MongoClient(self.MONGO_URL, self.MONGO_PORT)
        db = con[self.MONGO_DB][self.MONGO_COLLECTION]
        cur = db.find({"logsource": logsource}).sort("log_seq_index", -1).limit(1)
        if cur.count() != 0:
            lastIndex = cur[0]["log_seq_index"]

        cur.close()
        con.close()
        return lastIndex

    def getUniqueServerLocations(self):
        logsourcelist = []
        con = MongoClient(self.MONGO_URL, self.MONGO_PORT)
        db = con[self.MONGO_DB][self.MONGO_COLLECTION_SERVER_DATA]
        cur = db.distinct("logsource")
        for c in cur:
            logsourcelist.append(str(c))
        con.close()
        return logsourcelist


# def test():
#     process = subprocess.run(['ps', '-aux'],
#                              stdout=subprocess.PIPE,
#                              universal_newlines=True)
#     out = process.stdout.split("\n")
#     pids = []
#     for o in out:
#         if o.__contains__("LogCollectDaemon.py"):
#             print("Found: \n", o)
#             r = o.split(" ")[5]
#             pids.append(r)
#
#     return pids
#
#
# def killBackgroundProcess(id):
#     process = subprocess.run(['kill', '-9', str(id)],
#                              stdout=subprocess.PIPE,
#                              universal_newlines=True)
#     print("Killing process...", id, " done")


if __name__ == '__main__':
    # s = test()
    # print(s)
    # for i in s:
    #     killBackgroundProcess(i)
    # time.sleep(3)
    d = RunDaemon()
    d.run()
