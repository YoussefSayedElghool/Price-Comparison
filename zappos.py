from bs4 import BeautifulSoup
import requests


HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})

class Zappos:
    
    def __init__(self, user_input : str):
        
        user_text = user_input
        self.URL = f"https://www.zappos.com/{user_text}"
        webpage = requests.get(self.URL, headers=HEADERS)
        self.soup = BeautifulSoup(webpage.content, "html.parser")
        self.container = self.soup.find('div', {'id':'products'})
        self.products_section = self.container.find_all('article')
        self.NUMBER_OF_PRODUCTS = 5
        
    def get_product_details(self):
        # Products Data
        
        products_list = self.products_section
        
        self.resultList = []
        
        for product in products_list:
            
            p_section_parts = list(product.children)
            top_part = p_section_parts[1]
            bottom_part = p_section_parts[2] 

            # Product name
            p_name = bottom_part.find('dd', {'itemprop': 'name'}).text
            
            # Product link
            p_link = p_section_parts[0].get('href') if len(p_section_parts) > 0 and p_section_parts[0].get('href') else None
            p_link = "https://www.zappos.com" + p_link
            
            # Product base price
            p_base_price = bottom_part.find('span', {'itemprop': 'price'}).text if bottom_part and bottom_part.find('span', {'itemprop': 'price'}) else None
            
            # Discount price
            p_check = bottom_part.find('span', {'itemprop': 'price'})
            
            if p_check:
                p_disc_price = p_check.next_element
                
            
            # Product image
            p_img = top_part.find('meta', {'itemprop': 'image'}).get('content') if top_part and top_part.find('meta', {'itemprop': 'image'}) else None
            
            # Product stars
            p_stars = bottom_part.find('span', {'class': 'sr-only'}).text[6] if bottom_part and bottom_part.find('span', {'class': 'sr-only'}) else None
            
            # Product rating
            p_rating = bottom_part.find('meta', {'itemprop': 'reviewCount ratingCount'}).get('content') if bottom_part and bottom_part.find('meta', {'itemprop': 'reviewCount ratingCount'}) else None

            pds_data = {
            'p_name': p_name ,
            'p_link': p_link,
            'p_disc_price': p_disc_price,
            'p_base_price' : p_base_price,
            'p_img' : p_img ,
            'p_stars' : p_stars ,
            'p_rating' : p_rating,
            'source' : "Zappos"
            }

            self.resultList.append(pds_data)
            
        return self.resultList   


import json
test = Zappos('jeans')
print()
with open('outputTest.txt' , 'w') as f:
    f.write(json.dumps(test.get_product_details()))