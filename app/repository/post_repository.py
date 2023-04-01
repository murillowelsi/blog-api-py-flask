from app.database import db
from app.model.post_model import Post


class PostRepository:

    def get_all_posts(self, sort_by='id'):
        if sort_by == 'created_at':
            posts = Post.query.order_by(Post.created_at).all()
        else:
            posts = Post.query.order_by(Post.id).all()

        return posts

    def get_post_by_id(self, post_id):
        post = Post.query.get(post_id)

        if post:
            return post
        else:
            return None

    @staticmethod
    def create_post(title, body):
        post = Post(title=title, body=body)
        db.session.add(post)
        db.session.commit()
        return post

    def delete_post_by_id(self, post_id):
        post = Post.query.get(post_id)

        if post:
            db.session.delete(post)
            db.session.commit()
            return True
        else:
            return False

    def update_post_by_id(self, post_id, title=None, body=None):
        post = Post.query.get(post_id)

        if post:
            if title:
                post.title = title
            if body:
                post.body = body

            db.session.commit()
            return post.to_dict()
        else:
            return None

