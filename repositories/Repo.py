# pip install peewee
import peewee 
from playhouse.shortcuts import model_to_dict
import Models as models
from flask_bcrypt import check_password_hash , generate_password_hash

class BaseRepo:
    def __init__(self, model):
        self.model = model

    def create(self, **kwargs):
        return self.model.create(**kwargs)

    def read_all(self):
        return [model_to_dict(obj) for obj in self.model.select()]

    def read_by_id(self, obj_id):
        try:
            obj = self.model.get_by_id(obj_id)
            return model_to_dict(obj)
        except peewee.DoesNotExist:
            return None

    def update(self, obj_id, **kwargs):
        query = self.model.update(**kwargs).where(self.model.id == obj_id)
        query.execute()
        return self.read_by_id(obj_id)

    def delete(self, obj_id):
        query = self.model.delete().where(self.model.id == obj_id)
        query.execute()

class CartRepo(BaseRepo):
    def __init__(self):
        super().__init__(models.Cart)
    def get_by_user_id(self, user_id):
        try:
            cart = models.Cart.select().where(models.Cart.user_id == user_id)
            return cart
        except models.Cart.DoesNotExist:
            return None
    
    def create(self, product_id  , user_id ):
        return models.models.Cart.create( product_id = product_id ,user_id = user_id )



class UsersRepo(BaseRepo):
    def __init__(self):
        super().__init__(models.Users)
    def verify_user(self, email, password):
        user = models.Users.get_or_none(models.Users.email == email)
        # if user and check_password_hash(user.hashed_password, password):
        if user and user.hashed_password ==  password:
            return user
        return None
    
    def register(self, first_name, last_name, email, password):
        # user = models.Users.create(name=name, phone=phone, email=email, hashed_password=generate_password_hash(password).decode('utf8'), image=image)
        user = models.Users.create(first_name = first_name, last_name = last_name, email = email , hashed_password = password )
        return user
    
   


class ProductsRepo(BaseRepo):
    def __init__(self):
         super().__init__(models.Users)
    
    def create(self, name, image, link, price, rating, stars, source):
        return models.Products.create(name = name , image = image, link = link, price = price, rating = rating, stars = stars, source = source)

cart_repo = CartRepo()
users_repo = UsersRepo()
products_repo = ProductsRepo()
