from flask import Blueprint, jsonify, request

from app.service.post_service import PostService

bp = Blueprint('posts', __name__)
post_service = PostService()


@bp.route('/posts', methods=['GET'])
def get_all_posts():
    sort_by = request.args.get('sort', 'id')
    posts = post_service.get_all_posts(sort_by=sort_by)
    return jsonify(posts)


@bp.route('/posts/<int:id>', methods=['GET'])
def get_post_by_id(id):
    post = post_service.get_post_by_id(id)
    if post is None:
        return jsonify({'error': 'Post not found'}), 404
    return jsonify(post)


@bp.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    title = data.get('title')
    body = data.get('body')
    if title is None or body is None:
        return jsonify({'error': 'Title and body are required'}), 400
    post = post_service.create_post(title=title, body=body)
    return jsonify(post), 201
