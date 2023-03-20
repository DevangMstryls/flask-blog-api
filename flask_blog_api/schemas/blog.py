from marshmallow import Schema, fields


class CreateBlogPostSchema(Schema):
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    is_published = fields.Bool()

class BlogPostSchema(Schema):
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    is_published = fields.Bool()
    created_at = fields.Str()
