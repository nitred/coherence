import json
import os
import random
import uuid

from factory import create_app, create_db
from flask import Flask, jsonify, request, send_from_directory
from gevent.wsgi import WSGIServer
from models import Action, Cookie, User, UserCookie, db

app = create_app()


@app.before_first_request
def init():
    print("Creating database.")
    create_db(app)


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route("/api/clickEvent", methods=['GET', 'POST'])
def register_click_event():
    print("clickEvent data: {}".format(request.json))
    return jsonify("clickEvent - Success")


@app.route("/api/registerUser", methods=['GET', 'POST'])
def registerUser():
    print("nameEvent data: {}".format(request.json))
    name = request.json.get('name')
    name_exists = db.session.query(User.id).filter_by(name=name).scalar() is not None
    if name_exists:
        random_number = random.randint(1, 10000)
        name = name + str(random_number)
    user = User(name)
    db.session.add(user)
    db.session.commit()
    print(User.query.all())
    return jsonify({"name": name})


@app.route("/api/registerCookie", methods=['GET', 'POST'])
def registerCookie():
    print("registerCookie.request.json : {}".format(request.json))
    cookie_id = request.json.get('cookie_id')
    cookie = Cookie(cookie_id)
    db.session.add(cookie)
    db.session.commit()
    print(Cookie.query.all())
    return jsonify("registerCookie - Success")


@app.route("/api/registerUserAndCookie", methods=['GET', 'POST'])
def registerUserAndCookie():
    print("registerUserAndCookie.request.json : {}".format(request.json))
    cookie_id = request.json.get('cookie_id')
    name = str(request.json.get('name'))
    print("cookie_id", cookie_id)
    print("name", name, type(name))
    userCookie = UserCookie(name, cookie_id)
    db.session.add(userCookie)
    db.session.commit()
    print(UserCookie.query.all())
    return jsonify("registerUserCookie - Success")


@app.route("/api/registerAction", methods=['GET', 'POST'])
def registerAction():
    print("registerAction.request.json : {}".format(request.json))
    cookie_id = request.json.get('cookie_id')
    action = str(request.json.get('action'))
    details = str(request.json.get('details'))
    print("cookie_id", cookie_id)
    print("action", action)
    print("details", details)
    usercookie = UserCookie.query.filter(UserCookie.cookie == cookie_id).first()
    usercookie_id = usercookie.id
    usercookie_name = str(usercookie.user)
    print("usercookie_name", usercookie_name)
    actionDetails = Action(usercookie_id, action, details)
    db.session.add(actionDetails)
    db.session.commit()
    action_path = Action.query.filter(Action.usercookie_id == usercookie_id).all()
    action_path = [{"id": action.id,
                    "timestamp": action.date_created.strftime('%Y-%m-%d_%H:%M:%S'),
                    "action": action.action,
                    "details": action.details,
                    "name": usercookie_name} for action in action_path]
    # print(action_path)
    return jsonify(action_path)


@app.route("/api/getAllPaths", methods=['GET', 'POST'])
def getAllPaths():
    actions = db.session.query(Action, UserCookie.user).join(UserCookie).all()
    print(actions)
    action_path = [{"id": action.id,
                    "timestamp": action.date_created.strftime('%Y-%m-%d_%H:%M:%S'),
                    "action": action.action,
                    "details": action.details,
                    "name": usercookie_name} for action, usercookie_name in actions]
    print(action_path)
    return jsonify(action_path)


if __name__ == "__main__":
    try:
        http_server = WSGIServer(('0.0.0.0', 8080), app)
        http_server.serve_forever()
    except Exception as exc:
        print(exc)
