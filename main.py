# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json

import numpy as np
import tornado.ioloop
from tornado import gen
from tornado.gen import multi
from tornado.httpclient import AsyncHTTPClient
from tornado.web import RequestHandler

import users

np.random.seed(0)
user_list = users.Users(num_users=1000)


class MainHandler(RequestHandler):
    def get(self):
        self.render("templates/index.html")


class SessionHandler(RequestHandler):
    def get(self):
        inactive_users = user_list.get_inactive_users()
        self.render("templates/session.html", users=inactive_users)


class TagHandler(RequestHandler):
    def get(self):
        if self.get_arguments("tag"):
            tags = self.get_arguments("tag")
            tags = [int(tag) for tag in tags]
            users_with_tag = user_list.get_users_with_tag(tags)
            self.render("templates/tags.html", users=users_with_tag, tags=tags)
        else:
            self.render("templates/tags.html", users=False, tags=False)

    def post(self):
        print(self.request)
        tags = self.get_arguments("tag")
        url = ["tag=" + tag for tag in tags]
        url = '&'.join(url)
        self.redirect("tags?" + url)


class StressTestHander(RequestHandler):
    async def get(self):
        http_client = AsyncHTTPClient()
        try:
            responses = await multi([http_client.fetch("http://localhost:8888/") for i in range(1000)])
            await self.render("templates/stress.html", responses=responses)

        except Exception as e:
            print("Error: %s" % e)


class UserInfoHandler(RequestHandler):
    def get(self, user_id):
        print(user_id)
        user = user_list.get_user_with_id(user_id)
        self.render("templates/user.html", user=user)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/session", SessionHandler),
        (r"/tags", TagHandler),
        (r"/stress", StressTestHander),
        (r"/users/([0-9]+)", UserInfoHandler),

    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
