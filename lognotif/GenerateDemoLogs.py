import syslog
import os
import time

SEVERITY_LEVELS = {
    '0': 'Emergency',
    '1': 'Alert',
    '2': 'Critical',
    '3': 'Error',
    '4': 'Warning'
}

SEVERITY_LEVELS_ENUM = {
    '0': syslog.LOG_EMERG,
    '1': syslog.LOG_ALERT,
    '2': syslog.LOG_CRIT,
    '3': syslog.LOG_ERR,
    '4': syslog.LOG_WARNING
}

LOG_COUNTS = {
    '0': 18,
    '1': 10,
    '2': 15,
    '3': 20,
    '4': 10
}


def generateLog(nLog, severity_lvl, ):
    for i in range(0, nLog):
        msg = SEVERITY_LEVELS[severity_lvl] + " Message-" + str(i)
        syslog.syslog(SEVERITY_LEVELS_ENUM[severity_lvl], msg)
        time.sleep(0.1)


if __name__ == '__main__':
    print("Genereting Logs...")
    for k in SEVERITY_LEVELS_ENUM.keys():
        generateLog(LOG_COUNTS[k], k)
    print("Finished Generating...")
