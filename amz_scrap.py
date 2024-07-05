import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def get_amazon_products(search_query):

    url = f'https://www.amazon.com/s?k={search_query.replace(" " , "+")}'.strip()
    options = Options()
    options.add_argument("--headless")  # Ensure headless mode is enabled
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--window-size=1920x1080")  # Set a standard window size
    options.add_argument("--no-sandbox")  # Disable sandbox mode
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument(f"user-agent={get_random_user_agent()}")

    # Initialize WebDriver
    service = Service(ChromeDriverManager())
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        
        # Introduce a random delay to mimic human behavior
        time.sleep(random.uniform(2, 5))
        
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # # price = soup.select_one('span[class="a-price"]').find('span', {'class': 'a-offscreen'}).get_text(strip=True)
        

        # p_link = soup.find('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')['href']
        # p_disc_price = soup.find('span', class_='a-offscreen').get_text(strip=True) if soup.find('span', class_='a-offscreen') else None
        # p_base_price = soup.find('span', class_='a-price a-text-price').find('span', attrs={'aria-hidden': 'true'}).get_text(strip=True) if soup.find('span', class_='a-price a-text-price') else None
        # p_img = soup.find('img', class_='s-image s-image-optimized-rendering')['src'] if soup.find('img', class_='s-image s-image-optimized-rendering') else None
        # p_stars = soup.find('span', class_='a-icon-alt').get_text(strip=True) if soup.find('span', class_='a-icon-alt') else None
        # p_rating = soup.find('span', class_='a-size-base s-underline-text').get_text(strip=True) if soup.find('span', class_='a-size-base s-underline-text') else None

        # print("Product Link:", p_link)
        # print("Discounted Price:", p_disc_price)
        # print("Base Price:", p_base_price)
        # print("Image Source:", p_img)
        # print("Stars:", p_stars)
        # print("Rating:", p_rating)



        # if price is None:
        #     raise ValueError("Price not found on the page.")
        
        # return price
          
        p_names = []
        for img in soup.find_all('img', class_='s-image s-image-optimized-rendering'):
            p_names.append(img['alt'].replace("Sponsored Ad - " , ""))

        p_links = []
        for link in soup.find_all('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'):
            p_links.append("https://www.amazon.com/" + link['href'])

        p_disc_prices = []
        for price in soup.find_all('span', class_='a-offscreen'):
            p_disc_prices.append(price.get_text(strip=True).replace("$" , ""))

        p_base_prices = []
        for price in soup.select('span[class="a-price"]'):
            price_span = price.find('span', {'class': 'a-offscreen'})
            if price_span:
                p_base_prices.append(price_span.get_text(strip=True).replace("$" , ""))
            else:
                p_base_prices.append(None)

        p_imgs = []
        for img in soup.find_all('img', class_='s-image s-image-optimized-rendering'):
            p_imgs.append(img['src'])

        p_stars = []
        for star in soup.find_all('span', class_='a-icon-alt'):
            p_stars.append(star.get_text(strip=True).replace(" out of 5 stars" , ""))

        p_ratings = []
        for rating in soup.find_all('span', class_='a-size-base s-underline-text'):
            p_ratings.append(rating.get_text(strip=True))

        min_len = min([len(p_links), len(p_disc_prices), len(p_base_prices), len(p_imgs), len(p_stars), len(p_ratings)])

        result_list = []
        for i in range(0, min_len):
            pds_data = {
            'p_name': p_names[i] ,
            'p_link':p_links[i],
            'p_disc_price':float(p_disc_prices[i]),
            'p_base_price':float(p_base_prices[i]),
            'p_img':p_imgs[i] ,
            'p_stars':p_stars[i] ,
            'p_rating':p_ratings[i],
            'source' : "Amazon"
            }
            result_list.append(pds_data)


        return result_list



    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        driver.quit()

# import json
# if __name__ == "__main__":
    
#     products = get_amazon_products("seliver watch rolex")
#     if products:
#         with open("test.txt" , 'w') as f:
#             f.write(json.dumps(products))
#         print(json.dumps(products))
#     else:
#         print("Could not retrieve the price of the product.")
