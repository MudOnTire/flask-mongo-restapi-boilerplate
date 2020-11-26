from mongoengine.queryset.base import NULLIFY
from mongoengine.fields import StringField, ReferenceField
from src.models.base import Base
from src.models.user import User


class Comment(Base):
    content = StringField(required=True, max_length=500)
    # when user deleted, author will be null
    author = ReferenceField(User, reverse_delete_rule=NULLIFY)
