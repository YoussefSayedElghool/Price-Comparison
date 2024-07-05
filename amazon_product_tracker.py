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

def get_amazon_product_price(url):
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
        
        # Extract the price using different possible selectors
        price = float(soup.select_one('span.aok-offscreen').get_text(strip=True)[1:])
        
        if price is None:
            raise ValueError("Price not found on the page.")
        
        return price
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        driver.quit()

# if __name__ == "__main__":
#     product_url = input("Enter the Amazon product URL: ").strip()
#     price = get_amazon_product_price(product_url)
#     if price:
#         print(f"The price of the product is: {price}")
#     else:
#         print("Could not retrieve the price of the product.")
