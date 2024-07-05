from bs4 import BeautifulSoup
import requests

HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})

class Shein_Product:
    
    def __init__(self, link : str):
        URL = link
        webpage = requests.get(URL, headers=HEADERS)
        self.soup = BeautifulSoup(webpage.content, "html.parser")
        
    def get_product_price(self):
        price = self.soup.find('div', {'class' : 'from original'}).get('aria-label')[1:]
        return float(price)
    
