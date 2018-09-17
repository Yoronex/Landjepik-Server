from models import *
from flask import Flask, request, abort, jsonify
import secrets

app = Flask(__name__)

teams = [Team(i) for i in range(0, 3)]
groups = []
zones = []
checkpoints = []

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
    return 'Hello, world!'

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
# {"token" = token.
#  "name" = String}
#
# Returns JSON output:
# {"success" = Boolean,
#  "error" = String | (NULL iff success==True)
def attack():
    if not request.json or not 'token' in request.json or not 'name' in request.json:
        abort(400)
    print(request.json.get('reply', ''))
    return jsonify({'reply': request.json.get('reply', '')})

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
#  "alert" = String | (can be NULL),
#  "type" = String["Info", "Warning", "Error", "Caught"] | (NULL iff "alert"==NULL)
#  "sound" = String | (can be NULL),
def updatePlayer():
    if not request.json or not 'token' in request.json or not 'lat' in request.json or not 'long' in request.json:
        abort(400)

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

if __name__ == '__main__':
    app.run(debug=True)


