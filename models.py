from datetime import datetime


class Zone:
    checkpoints = []

    def __init__(self, ob_id, name):
        self.id = ob_id
        self.name = name
        self.owner = None
        self.timeconquered = datetime.utcfromtimestamp(0)


class Conquer:
    def __init__(self, zone_id):
        self.zone = zone_id
        self.timeConquered = datetime.utcnow()
        self.points = 0
        self.pointspm = 0


class Team:
    checkpoints = []
    conquers = []
    groups = []

    def __init__(self, ob_id, name):
        self.id = ob_id
        self.name = name
        self.points = 0
        self.pointspm = 0


class Group:
    # global team, token, members, notifications
    members = []
    notifications = []

    def __init__(self, ob_id, token, team):
        self.id = ob_id
        self.token = token
        self.team = team

    def addMember(self, member):
        self.members.append(member)


class Checkpoint:
    def __init__(self, name, zone, lat, long):
        self.name = name
        self.zone = zone
        self.lat = lat
        self.long = long
