from mongoengine.document import Document
from mongoengine.fields import StringField
from src.common.enums import USER_ROLES
from src.models.base import Base


class User(Base):
    name = StringField(required=True, max_length=50)
    password = StringField(required=True, max_length=50)
    role = StringField(required=True, choices=USER_ROLES, default='user')