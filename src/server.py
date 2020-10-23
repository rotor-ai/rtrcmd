from flask import Flask, jsonify, Response
from flask.views import MethodView


"""
Endpoint class, used by the server class
"""
class Endpoint(MethodView):

    def __init__(self, get_func, post_func):
        self.get_func = get_func
        self.post_func = post_func

    def get(self):
        response = self.get_func()
        if response is not None:
            return response
        else:
            return ""

    def post(self):
        response = self.post_func()
        if response is not None:
            return response
        else:
            return ""

"""
Server object that can be provided get and post functions. Currently only creates a single endpoint.
"""
class Server(object):

    # Constructor
    # @param name: Name of the server
    # @param url: Url of the endpoint
    def __init__(self, name, url):
        self.name = name
        self.app = Flask(name)
        self.url = url
        self.post_func = None
        self.get_func = None

    # Add a function to the post endpoint. Values returned from the function will be the response to the post endpoint
    def add_post_method(self, post_func):
        self.post_func = post_func

    # Add a function to the get endpoint. Values returned from the function will be the response to the get endpoint
    def add_get_method(self, get_func):
        self.get_func = get_func

    # Start running the server
    def run(self, debug=False):
        if self.post_func is not None and self.get_func is not None:
            self.app.add_url_rule(self.url, view_func=Endpoint.as_view(self.name, get_func=self.get_func,
                                                                       post_func=self.post_func))
            self.app.run(debug)


if __name__ == '__main__':

    def get():
        return "This is the get function"

    def post():
        return "This is the post function"

    server = Server('Test Name', '/api')
    server.add_get_method(get)
    server.add_post_method(post)
    server.run()
