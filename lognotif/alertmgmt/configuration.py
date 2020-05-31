
MONGO_URL = "localhost"
MONGO_PORT = 27017
MONGO_DB = "LogNotifier"
MONGO_COLLECTION = "alert_log"
MONGO_COLLECTION_SERVER_DATA = "server_data"
MONGO_COLLECTION_TICKETS = "tickets"

SEVERITY_LEVELS = {
    '-1': 'None',
    '0': 'Emergency',
    '1': 'Alert',
    '2': 'Critical',
    '3': 'Error',
    '4': 'Warning',
    # '5': 'Notice',
    # '6': 'Informational',
    # '7': 'Debug',
}

SEVERITY_COLOR_CODE = {
    '0': 'red',
    '1': 'red',
    '2': 'red',
    '3': 'orange',
    '4': 'blue',
        '5': 'green',
        '6': 'green',
        '7': 'white',
}

SEVERITY_COLOR_CODE_RGBA = {
    'None': '#ffffff',
    'Emergency': '#f44336',
    'Alert': '#f44336',
    'Critical': '#f44336',
    'Error': '#ff9800',
    'Warning': '#03a9f4',
    'Notice': '#4caf50',
    'Informational': '#4caf50',
    'Debug': '#4caf50'
}

LOG_SERVER_FILE = "/var/log/message.log"