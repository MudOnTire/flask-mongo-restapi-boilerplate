from datetime import datetime
from flask_restful import Resource, reqparse
from src.common.utils import updateDocFields

from src.models.post import Post
from src.api.base import query, delete, get, update, authenticate

# post
post_args = reqparse.RequestParser()
post_args.add_argument("title",
                       type=str,
                       help="Post title is required",
                       required=True)
post_args.add_argument("content",
                       type=str,
                       help="Post content is required",
                       required=True)

# put
put_args = reqparse.RequestParser()
put_args.add_argument("title", type=str)
put_args.add_argument("content", type=str)


# to populate referenced field or something
def doc_modifier(doc):
    obj = updateDocFields(doc)
    db_author = doc.author
    obj['author'] = updateDocFields(db_author)
    return obj


class PostsApi(Resource):
    # query
    def get(self):
        return query(Post, self, doc_modifier=doc_modifier)

    # create
    @authenticate
    def post(self, account):
        args = post_args.parse_args()
        new_post = Post(title=args['title'],
                        content=args['content'],
                        author=account['id'])
        saved = new_post.save()
        post = doc_modifier(saved)
        return post, 201

    # delete
    @authenticate
    def delete(self, account):
        return delete(Post, self)


class PostApi(Resource):
    # update
    @authenticate
    def put(self, id, account):
        args = put_args.parse_args()
        target = Post.objects.with_id(id)
        return update(target, args, doc_modifier=doc_modifier)

    # get single
    def get(self, id):
        return get(Post, id, self, doc_modifier=doc_modifier)