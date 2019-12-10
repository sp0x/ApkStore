from flask import Flask, jsonify, request, abort, send_file
from werkzeug.utils import secure_filename
from flask_sockets import Sockets
import os
from flask_cors import CORS

import packagestore


app = Flask(__name__)
CORS(app, supports_credentials=True)
sockets = Sockets(app)
ALLOWED_EXTENSIONS = ["apk"]

@app.route('/')
def hello_world():
    return 'Hello World!'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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


@sockets.route('/ws')
def handle_message(ws):
    while not ws.closed:
        message = ws.receive()
        if message is None:
            app.logger.info("No message received...")
            continue
        else:
            ws.send("{ \"type\": \"ping\"}")


# ws - push update checks
# http:
# version check
# package download
# package upload
# robot listing, just ip?

if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    print("Server listening on: http://0.0.0.0:" + str(5000))
    server.serve_forever()
    # app.run()
