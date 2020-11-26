from datetime import datetime
from flask_restful import Resource, reqparse
from src.common.utils import updateDocFields

from src.models.post import Post
from src.models.user import User
from src.api.base import query, delete, get

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


class PostsApi(Resource):
    # query
    def get(self):
        return query(Post, self)

    # create
    def post(self):
        args = post_args.parse_args()
        new_post = Post(title=args['title'],
                        content=args['content'])
        saved = new_post.save()
        post = updateDocFields(saved)
        return post, 201

    # delete
    def delete(self):
        return delete(Post, self)


class PostApi(Resource):
    # update
    def put(self, id):
        args = put_args.parse_args()
        target = Post.objects.with_id(id)
        for key, value in args.items():
            if value is not None:
                target[key] = value
        target['updatedTime'] = datetime.utcnow()
        saved = target.save()
        post = updateDocFields(saved)
        return post, 200

    # get single
    def get(self, id):
        return get(Post, id, self)