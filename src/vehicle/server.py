from flask import Flask, jsonify, Response, request, make_response
from flask.views import MethodView
import threading
from werkzeug.serving import make_server
import logging


class ServerThread(threading.Thread):

    def __init__(self, app, server_addr, port):
        threading.Thread.__init__(self)
        self._server_addr = server_addr
        self._server_port = port
        self._srv = make_server(server_addr, port, app)
        self._ctx = app.app_context()
        self._ctx.push()

    def run(self):
        logging.info(f"Serving on {self._server_addr}:{self._server_port}")
        self._srv.serve_forever()

    def shutdown(self):
        self._srv.shutdown()


class Endpoint(MethodView):

    def __init__(self, get_func, post_func):
        self.get_func = get_func
        self.post_func = post_func

    def get(self):
        try:
            response = self.get_func()
            if response is not None:
                return make_response(jsonify(response), 200)
            else:
                return make_response(jsonify({"status": "OK"}), 200)

        except Exception as e:
            error_msg = str(e)
            logging.error(error_msg)
            error_json = {'error': error_msg}
            return make_response(jsonify(error_json), 400)

    def post(self):
        try:

            json_in = {}
            if request.data:
                json_in = request.get_json()
            response = self.post_func(json_in, request.remote_addr)
            if response is not None:
                return response
            else:
                return make_response(jsonify({"status": "OK"}), 200)

        except Exception as e:
            error_msg = str(e)
            logging.error(error_msg)
            error_json = {'error': error_msg}
            return make_response(jsonify(error_json), 400)


class Server(object):

    def __init__(self, name, server_addr, port):
        self._name = name
        self._port = port
        self._server_addr = server_addr
        self._app = Flask(name)
        self._srv = ServerThread(self._app, self._server_addr, self._port)

    def add_endpoint(self, url, name, get_func=None, post_func=None):
        self._app.add_url_rule(url, view_func=Endpoint.as_view(name, get_func=get_func, post_func=post_func))

    def run(self, debug=False):

        self._srv.start()

    def stop(self):
        logging.info("Shutting down server")
        self._srv.shutdown()
