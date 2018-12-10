import datetime

from peewee import *

db = SqliteDatabase('datahoarder.db')


class SourceStatus(Model):
    source = CharField()
    status = CharField()
    added = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db  # This model uses the "people.db" database.


db.connect()
db.create_tables([SourceStatus])
