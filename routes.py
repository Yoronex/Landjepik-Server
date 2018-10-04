from models import *
from flask import Flask, request, abort, jsonify, render_template, Response
from math import sin, cos, sqrt, atan2, radians
import secrets
from console import Console

teams = [Team(i) for i in range(0, 3)]
distanceThreshold = 15
groups = []
zones = []
checkpoints = []

checkpoints.append("AAA")

def create_app():
    app = Flask(__name__)

    def initialize():
        global console
        console = Console()
        console.start()

    def interrupt():
        global console
        console.cancel()

    group = Group("abab", 1)
    group.addMember("Roy")
    groups.append(group)
    initialize()
    return app

app = create_app()

def findgroup(token):
    group = next((x for x in groups if x.token == request.json.get('token')), None)
    return group


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route('/')
def index():
    return Response('It works!')

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    print("Does it work?")
    if not request.json or not 'title' in request.json:
        print("Going to abort!")
        abort(400)
    print("Let's continue")
    print(request.json['title'])
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


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
    if(group == None and checkpoint == None):
        return jsonify({"success": False, "error":"Deze checkpoint of groep bestaat niet (meer)!"})
    if((datetime.utcnow() - checkpoint.getZone.timeConquered).total_seconds() < 180.0):
        return jsonify({"success": False, "error":"Deze zone nog tijdelijk geblokkeerd!"})
    if(checkpoint in group.team.checkpoints):
        return jsonify({"success": False, "error": "Je team heeft deze zone al veroverd!"})
    distance = calculateDistance(request.json.get('lat'), request.json.get('long'), checkpoint.lat, checkpoint.long)
    if(distance < distanceThreshold):
        return jsonify({"success": False, "error":"Je bent niet dichtbij genoeg dit checkpoint!"})

    group.team.checkpoints.append(checkpoint)
    count = 0
    for c in checkpoint.zone.checkpoints:
        if c in group.team.checkpoints:
            count += 1
    if count >= 3:
        oldteam = checkpoint.zone.owner
        oldteam.zones.remove(checkpoint.zone)
        checkpoint.zone.owner = group.team

        alert = {"alerttype": "success", "alert": "Je team heeft succesvol zone {} veroverd!".format(checkpoint.zone.name)}
        for g in group.team.groups:
            g.notifications.append(alert)
    return jsonify({'success': True})

@app.route('/api/v1.0/update', methods=["GET"])
# Returns JSON output:
# TBD
def updateScore():
    return jsonify()

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
        abort(400)

    group = findgroup(request.json.get("token"))
    if len(group.notifications) is not 0:
        alert = group.notifications.get(0)
        dict = {"success": True,
                "alerttype": alert["alerttype"],
                "alert": alert["alert"]}
    else:
        dict = {"success": True}
    return jsonify

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
    token = secrets.token_hex(16)
    group = Group(token, request.json.get('team'))
    for m in request.json.get('members'):
        print(str(m))
        group.addMember(m)
    groups.append(m)
    return jsonify({"success":True, "token":token})

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

def calculateScore():
    for t in teams:
        pointspm = 0
        now = datetime.utcnow()
        for c in t.conquers:
            diff = (now - c.timeConquered).seconds / 60
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

def console():
    while True:
        try:
            x = input(">>> ").split()

            if x[0] == "help":
                help = open('help.txt', 'r')
                print(help.read())
                help.close()
        except IndexError:
            print("Input niet correct. Typ help voor de syntax")



