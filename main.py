import secrets
import sys

from flask import Flask
from waitress import serve

import db
import logger

app = Flask(__name__)


@app.route("/getServerKey", methods=['GET'])
def get_server_key():
    return ""


# Generate an api key for use in the client software with a recognizable id.
# Optionally provide the port the client should use.
# If no port is provided the next available port above 9000 will be used.
def generate_api_key(tunnel_id, port=None):
    if db.is_id_in_use(tunnel_id):
        logger.error(f"Id {tunnel_id} is already in use. Please use another id to create a new api key")
        sys.exit()

    api_key = secrets.token_urlsafe(36)
    if port is None:
        port = (db.get_last_used_port() + 1)
    if db.is_port_in_use(port):
        logger.error(f"Port {port} is already in use. Please enter another port to create a new api key")
        sys.exit()
    db.add_tunnel(tunnel_id, api_key, port, 0)
    logger.info(f"Created new tunnel entry with id {tunnel_id} which will become avaiable on port {port}"
                f"\n api key: {api_key}")


def print_help():
    logger.info("\nGenerate:\nUse the command -generate with a desired identifier to generate a key for use in the "
                "tunneling software.\n"
                "The key will be stored locally on this machine and can be used to authorize requests between "
                "the tunnel client and server."
                "\nFormat: \"-generate TUNNEL_ID [optionally PORT]\"\n\n"
                "Server:\nRun the application without any arguments to start the server.")


def handle_command():
    if len(sys.argv) > 2 and sys.argv[1] == "-generate":
        if len(sys.argv) > 3:
            generate_api_key(sys.argv[2], int(sys.argv[3]))
        else:
            generate_api_key(sys.argv[2])
    elif sys.argv[1] == "-help":
        print_help()
    elif sys.argv[1] == "-truncate":
        db.truncate()
    else:
        logger.error("Wrong command line argument. Use -help for more information")


if __name__ == '__main__':
    db.init_db()
    if len(sys.argv) > 0:
        handle_command()
    else:
        logger.info("Starting revssh-server")
        serve(app, listen='*:8989')
