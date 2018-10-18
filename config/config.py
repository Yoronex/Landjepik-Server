from datetime import datetime, timedelta

goals = {
    'points': 100,
    'conquers': 15,
    'defences': 15,
    'possessed_zones': 4
}

distanceThreshold = 15.0  # meter
starttime = "18-10-2018 16:45" # Tijd dat het spel begint, in 20-10-2018 22:59 format


## Extra code (te negeren)
def returnstarttime():
    return datetime.strptime(starttime, '%d-%m-%Y %H:%M') + timedelta(hours=2)