from datetime import datetime
from mongoengine.document import Document
from mongoengine.fields import BooleanField, DateTimeField


class Base(Document):
    createdTime = DateTimeField(required=True, default=datetime.utcnow)
    updatedTime = DateTimeField(required=True, default=datetime.utcnow)
    deleted = BooleanField(required=True, default=False)
    meta = {'allow_inheritance': True, 'abstract': True}
