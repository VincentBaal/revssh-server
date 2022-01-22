from waitress import serve
from flask import Flask, request
import os
import logger
import sys
import json
import db

app = Flask(__name__)
config = None


@app.route("/login", methods=['POST'])
def login():
    request_data = request.get_json()
    if request_data['username'] == config["username"] and request_data['password'] == config["password"]:
        return "key"
    else:
        return "error"


@app.route("/getServerKey", methods=['GET'])
def get_server_key():
    return "serverkey"





def load_config():
    if not os.path.exists("./config.json"):
        logger.error("Could not find config.json file. Exiting")
        sys.exit()
    global config
    config = json.loads(open("./config.json").read())


if __name__ == '__main__':
    logger.info("Starting revssh-server")
    db.init_db()
    load_config()
    serve(app, listen='*:8989')
