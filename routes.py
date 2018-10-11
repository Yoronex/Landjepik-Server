from models import *
from flask import Flask, request, abort, jsonify, render_template, Response
from math import sin, cos, sqrt, atan2, radians
import secrets
import atexit
import threading
import sys
import os.path

teams = [Team(i, "Naamloos " + str(i)) for i in range(0, 3)]
distanceThreshold = 15.0
groups = []
zones = []
checkpoints = []

g1 = Group(len(groups), 'AAA', teams[1])
g1.addMember("Roy")
g1.addMember("Pietje")
g1.team.groups.append(g1)
groups.append(g1)


def create_app():
    app = Flask(__name__)

    def initialize():
        global t1
        t1 = threading.Thread(target=create_console)
        t1.daemon = True
        t1.start()
        t2 = threading.Thread(target=calculateScore)
        t2.daemon = True
        t2.start()
        #t2 = threading.Thread(target=calculateScore)
        #t2.daemon = True
        #t2.start()


    initialize()
    return app


def calculateScore():
    threading.Timer(1.0, calculateScore).start()
    now = datetime.utcnow()
    for t in teams:
        pointspm = 0
        for c in t.conquers:
            diff = int((now - c.timeConquered).seconds / 60)
            if diff > 10:
                points = 10 + (diff - 10) * 2
                pointspm = pointspm + 2
            else:
                points = diff
                pointspm = pointspm + 1

            if c.points != points:
                pointsdiff = points - c.points
                t.points = t.points + pointsdiff
        t.pointspm = pointspm


def create_console():
    t3 = threading.Thread(target=console)
    t3.daemon = True
    t3.start()
    t3.join()
    #func = request.environ.get('werkzeug.server.shutdown')
    #if func is None:
    #    raise RuntimeError('Not running with the Werkzeug Server')
    #func()
    sys.exit(4)
    print("Tot ziens!")

def load_zones():
    with open('zones.txt') as f:
        lines = f.readlines()
    try:
        for l in lines:
            zones
    except IndexError:
        print("ERROR: De input in het bestand is ongeldig.")
    f.close()


def console():
    while True:
        try:
            x = input(">>> ").split()

            if x[0] == "help":
                helpfile = open('help.txt', 'r')
                print(helpfile.read())
                helpfile.close()

            elif x[0] == "defend":
                attackers, defenders
                for g in groups:
                    if g.id == x[1]:
                        attackers = g
                    if g.id == x[2]:
                        defenders = g
                attackers.points = attackers.points - 5
                defenders.points = defenders.points + 2
                alert = {"alerttype": "Caught",
                         "alert": "Je bent betrapt door team {} en bent 5 punten verloren! Verlaat hun zone onmiddelijk!"
                             .format(defenders.team.name)}
                attackers.notifications.append(alert)
                alert = {"alerttype": "Success",
                         "alert": "Je hebt succesvol je zone verdedigd en 3 punten verdiend! "
                                  "Team {} zal het gebied zo snel mogelijk verlaten".format(attackers.team.name)}
                defenders.notifications.append(alert)
                print("SUCCESS: Team {} heeft de aanval van team {} afgeslagen".format(defenders.team.id, attackers.team.id))

            elif x[0] == "add":
                if x[1] == "checkpoints":
                    with open('checkpoints.txt') as f:
                        lines = f.readlines()
                    try:
                        for l in lines:
                            w = l.split()
                            zone = next((y for y in zones if y.id == int(w[1])), None)
                            if zone is None:
                                print("ERROR: Zone met ID {} bestaat niet!".format(w[1]))
                                continue
                            checkpoint = Checkpoint(str(w[0]), zone, float(w[2]), float(w[3]))
                            checkpoints.append(checkpoint)
                            zone.checkpoints.append(checkpoint)
                    except IndexError:
                        print("ERROR: De input in het bestand is ongeldig.")
                    f.close()

                elif x[1] == "team":
                    name = x[2]
                    teams.append(Team(len(teams), name))
                    print("SUCCESS: Team aangemaakt")

                elif x[1] == "group":
                    token = x[2]
                    team = next((t for t in teams if t.id == x[3]), None)
                    if team is None:
                        print("ERROR: Dit team bestaat niet!")
                    else:
                        g = Group(len(groups), token, team)
                        if len(x) <= 4:
                            raise IndexError("No members given")
                        for i in range(4, len(x)):
                            g.addMember(x[i])
                        print("SUCCESS: Groep toegevoegd")

                elif x[1] == "zone":
                    zones.append(Zone(len(zones), x[2]))

                elif x[1] == "notification":
                    group = next((g for g in groups if g.id == int(x[2])), None)
                    print(group.token)
                    message = ""
                    for y in range(4, len(x)):
                        message = message + " " + x[y]
                    alert = {"alerttype": x[3],
                             "alert": message}
                    group.notifications.append(alert)
                else:
                    raise IndexError("No second input")

            elif x[0] == "list":
                if x[1] == "checkpoints":
                    printCheckpoints(checkpoints)
                elif x[1] == "groups":
                    printGroups(groups)
                elif x[1] == "teams":
                    printTeams(teams)
                elif x[1] == "zones":
                    printZones(zones)

            elif x[0] == "quit":
                y = input("WARNING: Weet je het zeker? [y/n]")
                if y == "y":
                    break

            else:
                print('ERROR: Input niet correct. Typ "help" voor de syntax')
        except IndexError:
            print('ERROR: Input niet correct. Typ "help" voor de syntax')


def printCheckpoints(item):
    stringformat = "{:<8} {:<15} {:<10} {:<10}"
    print(stringformat.format('Naam', 'Zone', 'Lat', 'Long'))
    for i in item:
        print(stringformat.format(i.name, i.zone.name, i.lat, i.long))


def printGroups(item):
    stringformat = "{:<4} {:<10} {}"
    print(stringformat.format('ID', 'Team', 'Leden'))
    for i in item:
        print(stringformat.format(i.id, i.team.name, i.members))


def printTeams(item):
    print("Printing teams..." + str(len(item)))
    stringformat = "{:<4} {:<10} {}"
    print(stringformat.format('ID', 'Naam', 'Points'))
    for i in item:
        print(stringformat.format(i.id, i.name, i.points))

def printZones(item):
    stringformat = "{:<4} {:<10} {:<10} {}"
    print(stringformat.format('ID', 'Naam', 'Eigenaar', 'tijd'))
    for i in item:
        if i.owner is None:
            owner = "Niemand"
        else:
            owner = i.owner.name
        if i.timeconquered == datetime.utcfromtimestamp(0):
            time = "0:00:00"
        else:
            time = datetime.utcnow() - i.timeconquered
        print(stringformat.format(i.id, i.name, owner, time))

def findgroup(token):
    group = next((x for x in groups if x.token == token), None)
    return group


app = create_app()


@app.route('/')
def index():
    return Response('It works!')


@app.route('/api/v1.0/attack', methods=['POST'])
# Required JSON input:
# {"token" = token,
#  "name" = String,
#  "lat" = Float,
#  "long" = Float}
#
# Returns JSON output:
# {"success" = Boolean,
#  "error" = String | (NULL iff success==True)
def attack():
    if not request.json or not 'token' in request.json or not 'name' in request.json:
        abort(400)
    print(request.json.get('reply', ''))
    group = findgroup(request.json.get("token"))
    checkpoint = next((x for x in checkpoints if x.name == request.json.get('name')), None)
    if (group == None and checkpoint == None):
        return jsonify({"success": False, "error": "Deze checkpoint of groep bestaat niet (meer)!"})
    if ((datetime.utcnow() - checkpoint.zone.timeconquered).total_seconds() < 180.0):
        return jsonify({"success": False, "error": "Deze zone nog tijdelijk geblokkeerd!"})
    if (checkpoint in group.team.checkpoints):
        return jsonify({"success": False, "error": "Je team heeft deze checkpoint al!"})
    distance = calculateDistance(request.json.get('lat'), request.json.get('long'), checkpoint.lat, checkpoint.long)
    if (distance > distanceThreshold):
        return jsonify({"success": False, "error": "Je bent niet dichtbij genoeg dit checkpoint!"})

    group.team.checkpoints.append(checkpoint)
    count = 0
    for c in checkpoint.zone.checkpoints:
        if c in group.team.checkpoints:
            count += 1
    if count >= 3:
        zone = checkpoint.zone
        if zone.owner is not None:
            oldteam = zone.owner
            oldconquer = (c for c in oldteam.conquers if c.zone == zone)
            oldteam.conquers.delete(oldconquer)
        zone.owner = group.team
        group.team.conquers.append(Conquer(zone))
        zone.timeconquered = datetime.utcnow()

        for c in checkpoint.zone.checkpoints:
            if c in group.team.checkpoints:
                group.team.checkpoints.remove(c)

        alert = {"alerttype": "success",
                 "alert": "Je team heeft succesvol zone {} veroverd!".format(checkpoint.zone.name)}
        for g in group.team.groups:
            g.notifications.append(alert)
    return jsonify({'success': True})


@app.route('/api/v1.0/update', methods=["GET"])
# Returns JSON output:
# TBD
def updateScore():
    nestedDict = {}


    def updateZones():
        zoneDict = {}
        for z in zones:
            if z.owner is None:
                zoneDict[z.id] = None
            else:
                zoneDict[z.id] = z.owner.id
        nestedDict['zones'] = zoneDict


    def updatePoints():
        pointsDict = {}
        pointspmDict = {}
        for t in teams:
            pointsDict[t.id] = t.points
            pointspmDict[t.id] = t.pointspm
        nestedDict['points'] = pointsDict
        nestedDict['pointspm'] = pointspmDict

    updateZones()
    updatePoints()
    return jsonify(nestedDict)


@app.route('/api/v1.0/update', methods=['POST'])
# Required JSON input:
# {"token" = String,
#  "lat" = Float,
#  "long" = Float}
#
# Returns JSON output:
# {"success" = Boolean,
#  "alerttype" = String["Info", "Success, "Warning", "Error", "Caught"] | (NULL iff "alert"==NULL),
#  "alert" = String | (can be NULL),
#  "sound" = String | (can be NULL) }
def updatePlayer():
    if not request.json or not 'token' in request.json or not 'lat' in request.json or not 'long' in request.json:
        abort(404)

    group = findgroup(request.json.get("token"))

    group.lat = request.json.get('lat')
    group.long = request.json.get('long')

    if len(group.notifications) is not 0:
        alert = group.notifications[0]
        dict = {"success": True,
                "alerttype": alert["alerttype"],
                "alert": alert["alert"]}
        del group.notifications[0]
    else:
        dict = {"success": True,
                "alerttype": None,
                "alert": None}
    return jsonify(dict)


@app.route('/api/v1.0/create', methods=["POST"])
# Required JSON input:
# {"team" = int,
#  "members" = [String]}
#
# Returns JSON output:
# {"success" = Boolean,
#  "token" = String}
def create():
    if not request.json or not 'team' in request.json or not 'members' in request.json:
        abort(400)
    id = len(groups)

    if request.json.get('token') != None:
        token = request.json.get('token')
    else:
        token = secrets.token_hex(16)

    group = Group(id, token, request.json.get('team'))
    for m in request.json.get('members'):
        print(str(m))
        group.addMember(m)
    group.team.groups.append(group)
    groups.append(m)
    return jsonify({"success": True, "token": token})


def calculateDistance(lat1pre, long1pre, lat2pre, long2pre):
    R = 6371000.0

    lat1 = radians(lat1pre)
    lon1 = radians(long1pre)
    lat2 = radians(lat2pre)
    lon2 = radians(long2pre)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance