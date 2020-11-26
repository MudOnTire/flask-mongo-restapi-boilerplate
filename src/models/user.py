from enum import unique
from mongoengine.document import Document
from mongoengine.fields import StringField
from src.common.enums import USER_ROLES
from src.models.base import Base


class User(Base):
    name = StringField(required=True, unique=True, max_length=50)
    password = StringField(required=True)
    role = StringField(required=True, choices=USER_ROLES, default='user')