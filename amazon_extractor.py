from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome('/Users/weijithwimalasiri/Downloads/chromedriver-mac-arm64/chromedriver')

# Navigate to Amazon's homepage
driver.get("https://www.amazon.com/s?k=cricket+bats&crid=24GRHPUX0N1XF&sprefix=cricket+ba%2Caps%2C615&ref=nb_sb_noss_2")


# Define a function to scrape product information from the current page
def scrape_products():
    products = driver.find_elements(By.XPATH, "//div[contains(@class, 's-result-item')]")
    for product in products:
        try:
            # Extract product name
            name = product.find_element(By.XPATH, ".//span[@class='a-size-medium a-color-base a-text-normal']").text
        except:
            name = "N/A"
        
        try:
            # Extract product price (whole and fraction parts)
            price_whole = product.find_element(By.XPATH, ".//span[@class='a-price-whole']").text
            price_fraction = product.find_element(By.XPATH, ".//span[@class='a-price-fraction']").text
            price = f"${price_whole}.{price_fraction}"
        except:
            price = "N/A"
        
        try:
            # Extract product rating
            rating = product.find_element(By.XPATH, ".//span[@class='a-icon-alt']").get_attribute("innerHTML")
        except:
            rating = "N/A"
        
        try:
            # Extract availability (usually in stock information)
            availability = product.find_element(By.XPATH, ".//span[contains(@class, 'a-color-success')]").text
        except:
            availability = "Not specified"
        
        # Print the product details (or store in a database/file)
        print(f"Name: {name}")
        print(f"Price: {price}")
        print(f"Rating: {rating}")
        print(f"Availability: {availability}")
        print("-" * 40)

# Loop through multiple pages and scrape each one
def scrape_multiple_pages():
    page = 1
    while True:
        print(f"Scraping page {page}...")
        scrape_products()  # Scrape the current page
        
        try:
            # Wait for the next page button to be clickable
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 's-pagination-next')]"))
            )
            next_button.click()  # Click on the next page button
            
            # Wait for the next page to load before scraping
            time.sleep(3)
        except Exception as e:
            print("No more pages or an error occurred:", e)
            break  # Break the loop if there's no next button or an error occurs
        
        page += 1

# Start scraping multiple pages
scrape_multiple_pages()

# Close the driver after scraping is complete
driver.quit()
