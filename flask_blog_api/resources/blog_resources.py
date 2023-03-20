from flask import request
from flask_restful import Resource
from helpers.database import get_db_connection
from marshmallow import ValidationError
from schemas.blog import BlogPostSchema, CreateBlogPostSchema

create_blog_post_schema = CreateBlogPostSchema()
blog_post_schema = BlogPostSchema()
all_blog_posts_schema = BlogPostSchema(many=True)

class CreateBlogPostRoute(Resource):
    def post(self):
        try:
            payload = request.get_json(force=True)

            data = create_blog_post_schema.load(payload)

            title = data['title']
            content = data['content']
            is_published = data['is_published'] if 'is_published' in data else True

            db_conn = get_db_connection()
            cursor = db_conn.execute(
                "INSERT INTO posts (title, content, is_published) VALUES (?, ?, ?)",
                (title, content, is_published)
            )

            db_conn.commit()

            new_post = db_conn.execute(
                "SELECT * FROM posts WHERE id = ?",
                (cursor.lastrowid,)
            ).fetchone()

            db_conn.close()

            result = blog_post_schema.dump(new_post)

            return {
                'success': True,
                'data': result,
            }, 200
        except ValidationError as e:
            return {
                'success': False,
                'error': e.messages,
            }, 400
        except Exception as e:
            return {
                'success': False,
                'error': "Something went wrong. Please try again"
            }, 500

class BlogPostRoute(Resource):
    def get(self, post_id):
        try:
            db_conn = get_db_connection()
            post = db_conn.execute(
                "SELECT * FROM posts WHERE id = ?",
                (post_id,)
            ).fetchone()
            db_conn.close()

            # validations
            if post is None:
                return {
                    'success': False,
                    'error': 'Post does not exists'
                }, 404

            result = blog_post_schema.dump(post)

            return {
                'success': True,
                'data': result,
            }, 200
        except ValidationError as e:
            return {
                'success': False,
                'error': e.messages,
            }, 400
        except Exception as e:
            return {
                'success': False,
                'error': "Something went wrong. Please try again"
            }, 500


class AllBlogPostsRoute(Resource):
    def get(self):
        try:
            db_conn = get_db_connection()
            posts = db_conn.execute(
                "SELECT * FROM posts \
                ORDER BY created_at DESC \
                LIMIT 10"
            ).fetchall()
            db_conn.close()

            result = all_blog_posts_schema.dump(posts)

            return {
                'success': True,
                'data': result,
            }, 200
        except ValidationError as e:
            return {
                'success': False,
                'error': e.messages,
            }, 400
        except Exception as e:
            return {
                'success': False,
                'error': "Something went wrong. Please try again"
            }, 500
