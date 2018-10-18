from datetime import datetime, timedelta


class Zone:
    def __init__(self, ob_id, name, coordinates):
        self.id = ob_id
        self.name = name
        self.owner = None
        self.conquer = None
        self.timeconquered = datetime.utcfromtimestamp(0)
        self.checkpoints = []
        self.coordinates = coordinates


class Conquer:
    def __init__(self, zone_id):
        self.zone = zone_id
        self.timeConquered = datetime.utcnow()
        self.points = 0
        self.pointspm = 0


class Team:
    def __init__(self, ob_id, name, color):
        self.id = ob_id
        self.name = name
        self.points = 0
        self.pointspm = 0
        self.checkpoints = []
        self.conquers = []
        self.groups = []
        self.color = color
        self.defences = 0
        self.conquers_count = 0


class Group:
    def __init__(self, ob_id, token, team):
        self.id = ob_id
        self.token = token
        self.team = team
        self.members = []
        self.notifications = []

    def addMember(self, member):
        self.members.append(member)


class Checkpoint:
    def __init__(self, name, zone, lat, long):
        self.name = name
        self.zone = zone
        self.lat = lat
        self.long = long
