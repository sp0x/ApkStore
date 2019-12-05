from flask import Flask, jsonify
from flask_sockets import Sockets
import packagestore

app = Flask(__name__)
sockets = Sockets(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/package', methods=['POST'])
def upload_package():
    #Store the file
    packagename = ""
    packagepath = ""
    packagestore.put(packagename, packagepath)
    #Broadcast to all connected sockets that we have an event
    # { type : "update_push" }


@app.route('/api/<package>/version', methods=['GET'])
def version_check(package):
    from pyaxmlparser import APK
    if not packagestore.has(package):
        return ""
    path = packagestore.get(package)
    apk = APK(path)
    print(apk.package)
    print(apk.version_name)
    print(apk.version_code)
    print(apk.icon_info)
    print(apk.icon_data)
    print(apk.application)
    return jsonify({'version': apk.version_name})


@app.route('/api/<package>', methods=['GET'])
def get_package(package):
    file = packagestore.get(package)
    #return the file
    return file


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
