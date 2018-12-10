import datetime

from peewee import *

db = SqliteDatabase('datahoarder.db')


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
        downloads = Download.select()

        for d in downloads:
            d.delete_instance()

        statuses = SourceStatus.delete()
        statuses.execute()

    except DoesNotExist:
        return False
