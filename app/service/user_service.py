from app.repository.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def get_all_users(self, sort_by='id'):
        users = self.user_repository.get_all_users(sort_by=sort_by)
        return [user.to_dict() for user in users]

    def get_user_by_id(self, user_id):
        user = self.user_repository.get_user_by_id(user_id)
        if user:
            return user.to_dict()
        else:
            return None

    def create_user(self, username, password, email):
        user = self.user_repository.create_user(username=username, password=password, email=email)
        return user.to_dict()

    def delete_user_by_id(self, user_id):
        return self.user_repository.delete_user_by_id(user_id)

    def update_user_by_id(self, user_id, username=None, password=None, email=None):
        return self.user_repository.update_user_by_id(user_id, username=username, password=password, email=email)
