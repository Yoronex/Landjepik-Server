from datetime import datetime

class Zone():
    global owner, timeConquered
    owner = ""
    global checkpoints
    checkpoints = {}

    def setCheckpoints(self, name, coordinates):
        checkpoints[name] = coordinates

    def getCoordinates(self, name):
        return checkpoints[name]

    def setOwner(self, owner):
        self.owner = owner
        self.timeConquered = datetime.utcnow()

    def getOwner(self):
        return self.owner

    def getTimeConquered(self):
        return self.timeConquered

class Team():
    global id, points, pointspm, zones, location, locationtime, checkpoints, groups
    checkpoints = []

    def __init__(self, id):
        self.id = id

    def setPoints(self, points):
        self.points = points

    def getPoints(self):
        return self.points

    def setPointsPM(self, pointspm):
        self.pointspm = pointspm

    def getPointsPM(self):
        return self.pointspm

    def setLocation(self, location):
        self.location = location
        self.locationtime = datetime.utcnow()

    def getLocation(self):
        return self.location

    def getLocationTime(self):
        return self.locationtime

    def addCheckpoint(self, checkpoint):
        self.checkpoints.append(checkpoint)

    def removeCheckpoint(self, checkpoint):
        if checkpoint in self.checkpoints:
            self.checkpoints.remove(checkpoint)
            return True
        return False

    def getCheckpoints(self):
        return self.checkpoints

class Group():
    #global team, token, members, notifications
    members = []
    notifications = []

    def __init__(self, token, team):
        self.token = token
        self.team = team

    def addMember(self, member):
        self.members.append(member)

class Checkpoint():
    global name, zone

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setZone(self, zone):
        self.zone = zone

    def getZone(self):
        return self.zone
