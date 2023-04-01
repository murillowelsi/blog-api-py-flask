from app.database import db
from app.model.user_model import User


class UserRepository:

    def get_all_users(self, sort_by='id'):
        if sort_by == 'created_at':
            users = User.query.order_by(User.created_at).all()
        else:
            users = User.query.order_by(User.id).all()

        return users

    def get_user_by_id(self, user_id):
        user = User.query.get(user_id)

        if user:
            return user
        else:
            return None

    @staticmethod
    def create_user(username, email, password):
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return user

    def delete_user_by_id(self, user_id):
        user = User.query.get(user_id)

        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        else:
            return False

    def update_user_by_id(self, user_id, username=None, password=None, email=None):
        user = User.query.get(user_id)

        if user:
            if username:
                user.username = username
            if password:
                user.password = password
            if password:
                user.email = email

            db.session.commit()
            return user.to_dict()
        else:
            return None
