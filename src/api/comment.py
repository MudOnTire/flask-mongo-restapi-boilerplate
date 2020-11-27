from flask_restful import Resource, reqparse
from mongoengine.queryset.visitor import Q
from src.common.utils import updateDocFields

from src.models.comment import Comment
from src.api.base import delete, authenticate

# get
get_args = reqparse.RequestParser()
get_args.add_argument("type", type=str, default='post')
get_args.add_argument("target", type=str, required=True)
get_args.add_argument("page_index", type=int, default=1)
get_args.add_argument("page_size", type=int, default=10)

# post
post_args = reqparse.RequestParser()

post_args.add_argument("content",
                       type=str,
                       help="Comment content is required",
                       required=True)
post_args.add_argument("type",
                       type=str,
                       help="Comment type is required",
                       default='post')
post_args.add_argument("target",
                       type=str,
                       help="Comment target content is required",
                       required=True)


# to populate referenced field or something
def doc_modifier(doc):
    obj = updateDocFields(doc)
    db_author = doc.author
    obj['author'] = updateDocFields(db_author)
    return obj


class CommentsApi(Resource):
    # query
    def get(self):
        args = get_args.parse_args()
        print('args === ', args)
        page_index = args['page_index']
        page_size = args['page_size']
        result = []
        query = None
        type = args['type']
        target = args['target']
        if type == 'post':
            query = Comment.objects(
                Q(deleted__ne=True) & Q(type='post') & Q(post=target))
        if type == 'comment':
            query = Comment.objects(
                Q(deleted__ne=True) & Q(type='comment') & Q(comment=target))
        if query is None:
            return 400
        db_objs = query.skip((page_index - 1) * page_size).limit(page_size)
        for db_obj in db_objs:
            obj = doc_modifier(db_obj)
            del obj[type]
            result.append(obj)
        res = {
            'list': result,
            'pagination': {
                'current': page_index,
                'pageSize': page_size,
                'total': db_objs.count()
            }
        }
        return res, 200

    # create
    @authenticate
    def post(self, account):
        args = post_args.parse_args()
        type = args['type']
        new_comment = None
        if type == 'post':
            new_comment = Comment(content=args['content'],
                                  type='post',
                                  author=account['id'],
                                  post=args['target'])
        if type == 'comment':
            new_comment = Comment(content=args['content'],
                                  type='comment',
                                  author=account['id'],
                                  comment=args['target'])
        if new_comment is None:
            return 400
        saved = new_comment.save()
        comment = doc_modifier(saved)
        return comment, 201

    # delete
    @authenticate
    def delete(self, account):
        return delete(Comment, self)