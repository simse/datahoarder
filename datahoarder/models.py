import datetime
import os

from peewee import *


db = SqliteDatabase(os.environ.get('DH_CONFIG_PATH', '/config') + '/datahoarder.db')


class SourceStatus(Model):
    source = CharField()
    status = CharField()
    added = DateTimeField(default=datetime.datetime.now)

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
db.create_tables([SourceStatus, Download])


def clean_db():
    try:
        # Clear out database if possible
        downloads = Download.delete()
        downloads.execute()

        statuses = SourceStatus.delete()
        statuses.execute()

    except DoesNotExist:
        return False
