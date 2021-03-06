from pyrogram.types import Message, User
from mediacenter.database import database


class UserDB:
    def __init__(self):
        self.users = database()['users']

    def all_users(self):
        users = self.users.find()
        return users

    def all_user_ids(self):
        return [int(x['id']) for x in self.users.find({}, {'id': True})]

    def find_user(self, message: Message):
        query = {
            "id": message.chat.id
        }
        user = self.users.find_one(query)

        return user

    def create_user(self, message: Message):
        data = {
            "id": message.chat.id,
            "f_name": message.chat.first_name,
            "l_name": message.chat.last_name,
            "username": message.chat.username,
            'state': None,
            'module': 'home',
        }
        self.users.insert_one(data)
        return self.find_user(message)

    def create_user_with_id(self, user_id):
        user = self.users.find_one({
            "id": int(user_id)
        })

        if user:
            return
        else:
            self.users.insert_one({
                "id": int(user_id),
            })

    def update_user(self, message: Message):
        query = {
            "id": message.chat.id,
        }

        data = {
            "f_name": message.chat.first_name,
            "l_name": message.chat.last_name,
            "username": message.chat.username,
        }

        new_values = {"$set": data}

        self.users.update_one(query, new_values)
        return self.find_user(message)

    def find_or_create(self, message: Message):
        user = self.find_user(message)

        if user is None:
            self.create_user(message)
            user = self.find_user(message)

        return user

    def update_state(self, message: Message, state):
        query = {
            "id": message.chat.id,
        }

        data = {
            "state": state,
        }

        new_values = {"$set": data}

        self.users.update_one(query, new_values)

    def current_module(self, user: User):
        """
        Find the user's current in use module

        :param user:
        :return:
        """
        query = {
            "id": user.id
        }

        return self.users.find_one(query)['module']

    def set_module(self, user: User, module):
        """
        Set active module for user

        :param user:
        :param module:
        :return:
        """
        query = {"id": user.id}

        data = {"module": module}

        new_values = {"$set": data}

        return self.users.update(query, new_values)