from mongoengine.queryset.base import NULLIFY
from mongoengine.fields import StringField, ReferenceField, ListField
from src.models.base import Base
from src.models.user import User
from src.models.comment import Comment


class Post(Base):
    title = StringField(required=True, unique=True, max_length=100)
    content = StringField(required=True)
    # when user deleted, author will be null
    author = ReferenceField(User, reverse_delete_rule=NULLIFY)
    comments = ListField(ReferenceField(Comment))
