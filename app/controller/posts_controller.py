import os

from flasgger import swag_from
from flask import Blueprint, request

from app.service.post_service import PostService
from app.utils.util import create_json_response, create_error_response

base_path = '/Users/murillowelsi/PycharmProjects/blog-api/app/doc'

posts_bp = Blueprint('posts_bp', __name__)
post_service = PostService()


@posts_bp.route('/posts', methods=['GET'])
@swag_from(os.path.join(base_path, 'get_all_posts.yml'))
def get_all_posts():
    sort_by = request.args.get('sort', 'id')
    sort_column = 'created_at' if sort_by == 'created_at' else 'id'

    posts = post_service.get_all_posts(sort_by=sort_column)

    response_data = posts

    if sort_column == 'created_at':
        response_data = sorted(response_data, key=lambda k: k['created_at'])

    return create_json_response(response_data, 200)


@posts_bp.route('/posts/<int:id>', methods=['GET'])
@swag_from(os.path.join(base_path, 'get_post_by_id.yml'))
def get_post_by_id(id):
    post = post_service.get_post_by_id(id)

    if post is None:
        return create_error_response(404, 'Post not found')

    formatted_post = post
    return create_json_response(formatted_post, 200)


@posts_bp.route('/posts', methods=['POST'])
@swag_from(os.path.join(base_path, 'create_post.yml'))
def create_post():
    data = request.get_json()
    title, body = data.get('title'), data.get('body')

    post = post_service.create_post(title=title, body=body)

    response_data = post
    return create_json_response(response_data, 201)


@posts_bp.route('/posts/<int:id>', methods=['DELETE'])
@swag_from(os.path.join(base_path, 'delete_post_by_id.yml'))
def delete_post_by_id(id):
    success = post_service.delete_post_by_id(id)

    if success:
        return create_json_response({}, 204)
    else:
        return create_error_response(404, 'Post not found')


@posts_bp.route('/posts/<int:id>', methods=['PUT'])
@swag_from(os.path.join(base_path, 'update_post_by_id.yml'))
def update_post_by_id(id):
    data = request.get_json()
    title, body = data.get('title'), data.get('body')

    updated_post = post_service.update_post_by_id(id, title=title, body=body)

    if updated_post is None:
        return create_error_response(404, 'Post not found')

    response_data = updated_post
    return create_json_response(response_data, 200)
