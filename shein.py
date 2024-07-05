from bs4 import BeautifulSoup
import requests



HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})

class SheIn:
    
    def __init__(self, user_input : str):
        
        user_text = user_input
        URL = f"https://www.shein.com/pdsearch/{user_text}/?sort=7&source=sort&sourceStatus=1"
        webpage = requests.get(URL, headers=HEADERS)
        self.soup = BeautifulSoup(webpage.content, "html.parser")
        self.products_section = self.soup.find_all('section', {'class' : 'product-card multiple-row-card j-expose__product-item hover-effect product-list__item product-list__item-new', 'role' : 'listitem'})
        self.NUMBER_OF_PRODUCTS = 5
        
    def get_product_details(self):
        # Products Data
        products_list = self.products_section[:self.NUMBER_OF_PRODUCTS]
        self.resultList = []
        
        
        for product in products_list:
            
            p_section_parts = list(product.children)
            top_part = p_section_parts[0]
            bottom_part = p_section_parts[1]  
                      
            p_name = product.get('aria-label')
            p_link = 'https://www.shein.com' + bottom_part.find('a').get('href')
            p_img = 'https:' + top_part.find('div', {'class' : 'crop-image-container'}).get('data-before-crop-src')
            p_disc_price = bottom_part.find('div', {'class' : 'bottom-wrapper__price-wrapper'}).find('p', {'class' : 'product-item__camecase-wrap'})
            p_disc_price = float(p_disc_price.text.replace('$','')) if p_disc_price else 0
            
            
            discount_stamp = bottom_part.find('div', {'class': 'product-card__discount-label notranslate discount-label_discount'})
            discount_stamp = discount_stamp if discount_stamp else 0
            p_disc_stamp = float(discount_stamp.text[1:-1].replace("$" , "")) if discount_stamp else 0
            p_base_price = p_disc_price / (1 - (p_disc_stamp / 100))

            
            strs = bottom_part.find('div', {'class' : 'product-card__selling-proposition-star'})
            rate = bottom_part.find('div', {'class' : 'product-card__selling-proposition-star'})
                        
            if strs:
                p_stars = len(strs.find('ul', {'class' : 'star-icon-list'}))
            else:
                p_stars = None

            if rate:    
                p_rating = rate.find('p', {'class' : 'start-text'}).text.strip()[1:-1]
            else:
                p_rating = None

            pd_data = {
            'p_name': p_name,
            'p_link': p_link,
            'p_disc_price':p_disc_price,
            'p_base_price' : p_base_price,
            'p_img' : p_img,
            'p_stars' : p_stars,
            'p_rating' : p_rating,
            'source' : "Shein"
            }
            
            self.resultList.append(pd_data)
                
        # self.pds_data['p_price'] = list(map(float, self.pds_data['p_price']))
        return self.resultList    



test = SheIn('jeans')
# print(test.get_product_details())
