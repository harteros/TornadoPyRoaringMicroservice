# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json

import numpy as np
import tornado.ioloop
import tornado.web

import users

np.random.seed(0)
user_list = users.Users(num_users=1000)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class SessionHandler(tornado.web.RequestHandler):
    def get(self):
        inactive_users = user_list.get_inactive_users()
        self.write("Number of users that haven't logged in for at least 7 days: " + str(len(inactive_users)))


class TagHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("gg")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/session", SessionHandler),
        (r"/tags", TagHandler),

    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
