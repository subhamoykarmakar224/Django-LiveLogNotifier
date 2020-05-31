import threading
from pymongo import MongoClient
import datetime, time
from os import listdir
from os.path import isfile, join


class LogCycleDaemon:
    def __init__(self):
        super(LogCycleDaemon, self).__init__()
        self.thread_stop_flag = True
        self.MONGO_URL = "localhost"
        self.MONGO_PORT = 27017
        self.MONGO_DB = "LogNotifier"
        self.MONGO_COLLECTION = "alert_log"
        self.NO_OF_DAYS_LOG_CYCLE = 15
        self.SLEEPER = 43200 # every 12 hrs
        self.DATA_SIZE = 1000
        self._PATH = './zarchive/'

    def run(self):
        t1 = threading.Thread(target=self.job, name='Thread-log-archival', args=())
        t1.start()

    def job(self):
        while self.thread_stop_flag:
            d = datetime.datetime.now() - datetime.timedelta(days=self.NO_OF_DAYS_LOG_CYCLE)
            cnt = self.getLogCountBeforeDays(d)
            if cnt > 0:
                print("Archiving...")
                self.archiveLogs(d)
                print("Done archiving...")
                print("Cleaning db...")
                self.deleteArchivedLogs(d)
                print("Done...")


            time.sleep(self.SLEEPER)

    def getLogCountBeforeDays(self, date):
        con = MongoClient(self.MONGO_URL, self.MONGO_PORT)
        db = con[self.MONGO_DB][self.MONGO_COLLECTION]
        cnt = db.find({"datetimestamp": {'$lt': date}}).count()
        con.close()
        return cnt

    def logDataForArchival(self, d):
        con = MongoClient(self.MONGO_URL, self.MONGO_PORT)
        db = con[self.MONGO_DB][self.MONGO_COLLECTION]
        cur = db.find({"datetimestamp": {'$lt': d}}).sort("datetimestamp", -1)
        d = list(cur)
        con.close()
        return d

    def getLastFile(self):
        path = self._PATH
        fileslist = [f for f in listdir(path) if isfile(join(path, f))]
        lastIndex = 0
        for f in fileslist:
            tmp = f[f.index("_") + 1:f.index(".txt")]
            if int(tmp) > lastIndex:
                lastIndex = int(tmp)
        return lastIndex + 1

    def deleteArchivedLogs(self, d):
        con = MongoClient(self.MONGO_URL, self.MONGO_PORT)
        db = con[self.MONGO_DB][self.MONGO_COLLECTION]
        db.delete_many({"datetimestamp": {'$lt': d}})
        con.close()

    def archiveLogs(self, d):
        logdata = self.logDataForArchival(d)
        newCnt = self.getLastFile()
        curCnt = 1
        f = open(self._PATH + "log_" + str(newCnt) + ".txt", "a")
        for l in logdata:
            if curCnt == 100:
                curCnt = 1
                f.close()
                newCnt += 1
                f = open(self._PATH + "log_" + str(newCnt) + ".txt", "a")
            f.write(str(l) + "\n")
            curCnt += 1
        f.close()


if __name__ == '__main__':
    d = LogCycleDaemon()
    d.run()
