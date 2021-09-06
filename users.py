from datetime import datetime
from json import JSONEncoder

from pyroaring import BitMap

import utils


class User:

    def __init__(self, idx, tags, login_date):
        self.id = "User" + str(idx)
        self.tags = tags
        self.login_date = login_date


class Users:

    def __init__(self, num_users=100):
        self.users = []
        self.gen_random_users(num_users)

    def __len__(self):
        return len(self.users)

    def gen_random_users(self, num_users):
        self.users = [User(idx, utils.gen_random_tags(), utils.gen_random_date()) for idx in range(num_users)]

    def get_inactive_users(self):
        return [user for user in self.users if (datetime.today() - user.login_date).days > 7]

    def get_users_with_tag(self, tags):
        return [user for user in self.users if BitMap(tags).issubset(user.tags)]


class UserEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%d-%m-%Y')
        if isinstance(obj, BitMap):
            return list(obj)
        return obj.__dict__
