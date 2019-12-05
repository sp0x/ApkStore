from flask import Flask
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/package', methods=['POST'])
def upload_package():
    pass


@app.route('/api/<package>/version', methods=['GET'])
def version_check(package):
    return ""


@app.route('/api/<package>', methods=['GET'])
def get_package(package):
    pass


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
