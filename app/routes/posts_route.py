import os

from flasgger import swag_from
from flask import Blueprint, request, jsonify

from app.database import connect

base_path = '/Users/murillowelsi/PycharmProjects/blog-api/app/doc'


bp = Blueprint('routes', __name__)
conn = connect()

with conn.cursor() as cur:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT NOW()
        )
    """)
    conn.commit()


@bp.route('/posts', methods=['GET'])
@swag_from(os.path.join(base_path, 'get_all_posts.yml'))
def get_all_posts():
    sort_by = request.args.get('sort', 'id')
    sort_column = 'created_at' if sort_by == 'created_at' else 'id'

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, title, body, created_at
                FROM posts
                ORDER BY {}
            """.format(sort_column))
            posts = cur.fetchall()

    formatted_posts = [format_post(post) for post in posts]

    if sort_column == 'created_at':
        formatted_posts = sorted(formatted_posts, key=lambda k: k['created_at'])

    response_data = {'posts': formatted_posts}
    return create_json_response(response_data, 200)


@bp.route('/posts/<int:id>', methods=['GET'])
@swag_from(os.path.join(base_path, 'get_post_by_id.yml'))
def get_post_by_id(id):
    post = get_post_from_database(id)

    if post is None:
        return create_error_response(404, 'Post not found')

    formatted_post = format_post(post)
    return create_json_response(formatted_post, 200)


@bp.route('/posts', methods=['POST'])
@swag_from(os.path.join(base_path, 'create_post.yml'))
def create_post():
    data = request.get_json()
    title, body = data.get('title'), data.get('body')

    post_id = insert_post_in_database(title, body)

    response_data = {'id': post_id, 'title': title, 'body': body}
    return create_json_response(response_data, 201)


def get_post_from_database(post_id):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, title, body, created_at
            FROM posts
            WHERE id = %s
        """, (post_id,))
        post = cur.fetchone()

    return post


def format_post(post):
    return {'id': post[0], 'title': post[1], 'body': post[2], 'created_at': post[3]}


def insert_post_in_database(title, body):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO posts (title, body)
            VALUES (%s, %s)
            RETURNING id
        """, (title, body))
        post_id = cur.fetchone()[0]
        conn.commit()

    return post_id


def create_error_response(status_code, message):
    response_data = {'error': message}
    return create_json_response(response_data, status_code)


def create_json_response(response_data, status_code):
    response = jsonify(response_data)
    response.status_code = status_code
    return response
