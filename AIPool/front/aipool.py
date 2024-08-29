from flask import Flask, redirect, request, Response

application = Flask(__name__)

if __name__ == "__main__":
    debug = True
    application.run(host='0.0.0.0', debug=debug, use_reloader=debug, use_debugger=debug)