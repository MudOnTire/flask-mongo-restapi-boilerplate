from mongoengine.queryset.base import NULLIFY
from mongoengine.fields import StringField, ReferenceField
from mongoengine.queryset.base import CASCADE
from src.models.base import Base
from src.models.user import User
from src.models.post import Post
from src.common.enums import COMMENT_TARGET


class Comment(Base):
    content = StringField(required=True, max_length=500)
    # when user deleted, author will be null
    author = ReferenceField(User, reverse_delete_rule=NULLIFY)
    type = StringField(required=True, choices=COMMENT_TARGET, default='post')
    post = ReferenceField(Post, reverse_delete_rule=CASCADE)
    comment = ReferenceField('self', reverse_delete_rule=CASCADE)
