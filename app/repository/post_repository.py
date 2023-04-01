from app.database import db
from app.models.post_model import Post


class PostRepository:

    def get_all_posts(self, sort_by='id'):
        if sort_by == 'created_at':
            return Post.query.order_by(Post.created_at).all()
        else:
            return Post.query.order_by(Post.id).all()

    def get_post_by_id(self, post_id):
        return Post.query.get(post_id)

    def create_post(self, title, body):
        post = Post(title=title, body=body)
        db.session.add(post)
        db.session.commit()
        return post
