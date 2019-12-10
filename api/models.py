import sqlite3
from sqlite3 import Error
# from sqlite_orm.database import Database
# from sqlite_orm.field import IntegerField, BooleanField, TextField
# from sqlite_orm.table import BaseTable
from peewee import *

DB = "./db/main.sqlite"

db = SqliteDatabase(DB)
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class Package(BaseModel):
    name = CharField(unique=True)
    version = CharField(null=True)
    file = CharField(null=True)


db.create_tables([Package])
