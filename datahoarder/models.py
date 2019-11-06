import datetime
import os

from peewee import *


db = SqliteDatabase(os.environ.get('DH_CONFIG_PATH', '/config') + '/datahoarder.db')


class SourceModel(Model):
    uid = CharField()
    source_id = CharField()
    status = CharField(default='new')
    arguments = TextField()

    class Meta:
        database = db


class Download(Model):
    url = CharField()
    destination = CharField()
    progress = IntegerField(default=0)
    source = CharField()

    class Meta:
        database = db


db.connect()
db.create_tables([Download, SourceModel])


def clean_db():
    try:
        # Clear out database if possible
        downloads = Download.delete()
        downloads.execute()

    except DoesNotExist:
        return False
