from flask import Flask , jsonify, request , render_template, session, redirect, url_for
from flask_cors import CORS
from routes import register_blueprints
import sys
import os
import Models as models   
# from amz_scrap import get_amazon_product_price
import pickle
# from playhouse.shortcuts import model_to_dict
from flask_caching import Cache
import main 
from apscheduler.schedulers.background import BackgroundScheduler
import amazon_product_tracker
import zappos_product_tracker
import shein_product_tracker
# from repositories.Repo import *
from send_email import sende_email


# pip install APScheduler

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


app = Flask(__name__)

CORS(app, supports_credentials=True) 
app.secret_key = 'gA`3Nd%Uojfz3sUP8xjW6rHOm=5rm=$Ooy?_#,rSem6'
app.config['CACHE_TYPE'] = 'SimpleCache' 
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)

register_blueprints(app)




@app.route('/api/search/<string:query>', methods=['GET'])
@cache.cached(timeout=60)
def search(query):
    result = main.search(query)
    return result, 200

# @app.route('/api/test/<string:query>', methods=['GET'])
# def sff(query):
    
#     return get_amazon_product_price('https://www.amazon.com/s?k=jeans'), 200


@app.route('/api/model/<string:query>', methods=['GET'])
def model_test(query):
    with open("knn.pickle", 'rb') as file:
        model = pickle.load(file)
    with open('vect.pickle', 'rb') as file2:
        loaded_vectorizer  = pickle.load(file2)

    with open('mlb.pickle', 'rb') as file3:
        mlb  = pickle.load(file3)

    result = model.predict(loaded_vectorizer.transform([query]))
    result = mlb.inverse_transform(result)[0][0]
    return str(result)  , 200

def Notify(user_id : int , product_id : int , product_name : str , old_price: float , new_price: float ):
    User = models.Users.select(models.Users.email).where(models.Users.user_id == user_id)
    
    message =   f""" 
                Apply now to the offer on the {product_name} for {new_price}$ instead of {old_price}$
                 """
    
    sende_email(message , User.email)
    models.Notifications.create(user_id = user_id , product_id = product_id , message = message)





def scheduled_task():
    with app.app_context():

        for product in models.Cart.select(models.Cart.user_id , models.Products.product_id , models.Products.name , models.Products.price , models.Products.source  ).join(models.Products , on=(models.Cart.cart_id == models.Products.product_id)).dicts():
            source = str(product.source).lower()
            link = str(product.link)
            price = float(product.price)
            user_id = float(product.user_id)
            name = float(product.name)
            product_id = float(product.product_id)
            if source == "amazon":
                
                new_price = amazon_product_tracker.get_amazon_product_price(link)
               
                if new_price < price:
                    Notify(user_id=user_id , product_name=name , old_price= price , new_price=new_price , product_id=product_id)
                    models.roducts(price = new_price).save()
                    
                
            elif source == "shein":
                new_price = shein_product_tracker.Shein_Product(link).get_product_price()
                if new_price < price:
                    Notify(user_id=user_id , product_name=name , old_price= price , new_price=new_price , product_id=product_id)
                    models.Products(price = new_price).save()
                    
            elif source == "zappos":
                new_price = zappos_product_tracker.Zappos_Product(link).get_product_price()
                if new_price < price:
                    Notify(user_id=user_id , product_name=name , old_price= price , new_price=new_price , product_id=product_id)
                    models.Products(price = new_price).save()
                    


            





 




if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    # scheduler.add_job(scheduled_task, 'cron', hour=0, minute=1)
    scheduler.add_job(scheduled_task, 'interval' ,minutes=1)  
    scheduler.start()

    try:
            app.run(debug=True, port=5678, host='0.0.0.0') 
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        scheduler.shutdown()


    

