from app.repository.post_repository import PostRepository


class PostService:
    def __init__(self):
        self.post_repository = PostRepository()

    def get_all_posts(self, sort_by='id'):
        posts = self.post_repository.get_all_posts(sort_by=sort_by)
        return [post.to_dict() for post in posts]

    def get_post_by_id(self, post_id):
        post = self.post_repository.get_post_by_id(post_id)
        if post:
            return post.to_dict()
        else:
            return None

    def create_post(self, title, body):
        post = self.post_repository.create_post(title=title, body=body)
        return post.to_dict()
