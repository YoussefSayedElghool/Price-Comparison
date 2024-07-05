import peewee
import json

with open('config.json', 'r') as file:
    data = json.load(file)

db = peewee.MySQLDatabase(
    data["db_name"],
    user= data["db_user"],
    password= data["db_password"],
    host=data["db_host"],
    port=data["db_port"],
     charset=data["db_charset"]
     )


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Products(BaseModel):
    product_id = peewee.AutoField(primary_key=True)
    name = peewee.CharField()
    image = peewee.CharField()
    link = peewee.CharField()
    price = peewee.FloatField()
    disc_price = peewee.FloatField()
    rating = peewee.CharField(null=True)
    stars =  peewee.IntegerField(null=True)
    source = peewee.CharField()


class Users(BaseModel):
    user_id = peewee.AutoField(primary_key=True)
    name = peewee.CharField()
    phone = peewee.CharField()
    email = peewee.CharField(unique=True)
    hashed_password = peewee.CharField()

class Notifications(BaseModel):
    Notifi_id = peewee.AutoField(primary_key=True)
    user_id = peewee.ForeignKeyField(Users, backref='notifications')
    product_id = peewee.ForeignKeyField(Products, backref='notifications')
    message = peewee.CharField()

class Cart(BaseModel):
    cart_id = peewee.AutoField(primary_key=True)
    product_id = peewee.ForeignKeyField(Products, backref='carts' , unique = True)
    user_id = peewee.ForeignKeyField(Users, backref='carts')




db.connect()
db.create_tables([Products, Cart, Users , Notifications])

db.close()
