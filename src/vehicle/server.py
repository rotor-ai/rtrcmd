from flask import Flask, jsonify, Response, request, make_response
from flask.views import MethodView
import threading
from werkzeug.serving import make_server
import logging


class ServerThread(threading.Thread):

    def __init__(self, app, server_addr, port):
        threading.Thread.__init__(self)
        self.srv = make_server(server_addr, port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()


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
            error_json = {'error': str(e)}
            return make_response(jsonify(error_json), 400)

    def post(self):
        try:

            response = self.post_func(request.get_json())
            if response is not None:
                return response
            else:
                return make_response(jsonify({"status": "OK"}), 200)

        except Exception as e:
            error_json = {'error': str(e)}
            return make_response(jsonify(error_json), 400)


class Server(object):

    def __init__(self, name, server_addr, port):
        self.name = name
        self.port = port
        self.server_addr = server_addr
        self.app = Flask(name)
        self.srv = ServerThread(self.app, self.server_addr, self.port)

    def add_endpoint(self, url, get_func=None, post_func=None):
        self.app.add_url_rule(url, view_func=Endpoint.as_view(self.name, get_func=get_func, post_func=post_func))

    def run(self, debug=False):

        logging.info("Starting server on port {}".format(self.port))
        self.srv.start()

    def stop(self):
        logging.info("Shutting down server")
        self.srv.shutdown()


if __name__ == '__main__':

    def get():
        return "This is the get function"

    def post(json_in):
        print(json_in)
        return "This is the post function"

    server = Server('Test Name', '/api', 5000)
    server.add_get_method(get)
    server.add_post_method(post)
    server.run()
