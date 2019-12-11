from peewee import *
import os
DB = os.path.join(".", "db", "main.sqlite")

db = SqliteDatabase(DB)
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class Package(BaseModel):
    name = CharField(unique=True)
    version = CharField(null=True)
    file = CharField(null=True)


class Device(BaseModel):
    serial = CharField(unique=True)
    wifi_mac = CharField(null=True)
    imei = CharField(null=True)
    ext_ip = CharField(null=True)


class DevicePackage(BaseModel):
    device = ForeignKeyField(Device, backref='devicepackage')
    package = ForeignKeyField(Package, backref='devicepackage')
    version = CharField()


db.create_tables([Package, Device, DevicePackage])
