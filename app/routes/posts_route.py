import os

from flasgger import swag_from
from flask import Blueprint, request

from app.service.post_service import PostService
from app.utils.util import create_json_response, create_error_response

base_path = '/Users/murillowelsi/PycharmProjects/blog-api/app/doc'


bp = Blueprint('routes', __name__)
post_service = PostService()


@bp.route('/posts', methods=['GET'])
@swag_from(os.path.join(base_path, 'get_all_posts.yml'))
def get_all_posts():
    sort_by = request.args.get('sort', 'id')
    sort_column = 'created_at' if sort_by == 'created_at' else 'id'

    posts = post_service.get_all_posts(sort_by=sort_column)

    formatted_posts = posts

    if sort_column == 'created_at':
        formatted_posts = sorted(formatted_posts, key=lambda k: k['created_at'])

    response_data = {'posts': formatted_posts}
    return create_json_response(response_data, 200)


@bp.route('/posts/<int:id>', methods=['GET'])
@swag_from(os.path.join(base_path, 'get_post_by_id.yml'))
def get_post_by_id(id):
    post = post_service.get_post_by_id(id)

    if post is None:
        return create_error_response(404, 'Post not found')

    formatted_post = post
    return create_json_response(formatted_post, 200)


@bp.route('/posts', methods=['POST'])
@swag_from(os.path.join(base_path, 'create_post.yml'))
def create_post():
    data = request.get_json()
    title, body = data.get('title'), data.get('body')

    post = post_service.create_post(title=title, body=body)

    response_data = post
    return create_json_response(response_data, 201)

