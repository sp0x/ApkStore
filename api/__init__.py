from flask import Flask, jsonify, request, abort, send_file
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO
import os
from flask_cors import CORS
import packagestore

app = Flask(__name__)
CORS(app, supports_credentials=True)
# app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
ALLOWED_EXTENSIONS = ["apk"]
EV_PACKAGE_PUSHED = "update_push"

@app.route('/')
def hello_world():
    return 'Hello World!'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def broadcast_creation(pkginfo):
    ev = 'package_creation' if pkginfo['is_new'] else 'package_updated'
    payload = {
        "type": "update_push",
        "package": pkginfo["package"],
        "version": pkginfo["version"],
        "ev": ev
    }
    socketio.emit(EV_PACKAGE_PUSHED, payload, broadcast=True)


@app.route('/api/package', methods=['POST'])
def upload_package():
    if 'file' not in request.files:
        return abort(404)
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return abort(404)
    pkginfo = packagestore.put(file)
    # Broadcast to all connected sockets that we have an event
    # { type : "update_push" }
    broadcast_creation(pkginfo)
    return jsonify({
        "success": True,
        "pkginfo": pkginfo
    })


@app.route('/api/<package>/version', methods=['GET'])
def version_check(package):
    pkg = packagestore.has(package)
    if not pkg:
        return abort(404)
    return jsonify({'version': pkg.version})


@app.route('/api/<package>', methods=['GET'])
def get_package(package):
    pkg = packagestore.has(package)
    if not pkg:
        return abort(404)
    return send_file(pkg.file, mimetype='application/vnd.android.package-archive')


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))


# ws - push update checks
# http:
# version check
# package download
# package upload
# robot listing, just ip?

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
