from flask import Flask, jsonify, Response, request, make_response
from flask.views import MethodView
import threading
from werkzeug.serving import make_server
import logging


class ServerThread(threading.Thread):

    def __init__(self, app, port):
        threading.Thread.__init__(self)
        self.srv = make_server('0.0.0.0', port, app)
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

    def __init__(self, name, url, port):
        self.name = name
        self.port = port
        self.app = Flask(name)
        self.srv = ServerThread(self.app, port)
        self.url = url
        self.post_func = None
        self.get_func = None

    def add_post_method(self, post_func):
        self.post_func = post_func

    def add_get_method(self, get_func):
        self.get_func = get_func

    def run(self, debug=False):
        if self.post_func is not None and self.get_func is not None:
            self.app.add_url_rule(self.url, view_func=Endpoint.as_view(self.name, get_func=self.get_func,
                                                                       post_func=self.post_func))
            logging.info("Starting server on port {}".format(self.port))
            self.srv.start()

        else:
            raise Exception("No post or get functions provided")

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
