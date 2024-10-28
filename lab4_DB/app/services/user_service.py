from ..dao.user_dao import UserDAO

class UserService:
    def __init__(self):
        self.user_dao = UserDAO()

    def get_all_users(self):
        return self.user_dao.get_all()

    def get_user(self, user_id):
        return self.user_dao.get_by_id(user_id)

    def create_user(self, name, city_id):
        return self.user_dao.create(name, city_id)

    def update_user(self, user_id, name=None, city_id=None):
        return self.user_dao.update(user_id, name, city_id)

    def delete_user(self, user_id):
        return self.user_dao.delete(user_id)
