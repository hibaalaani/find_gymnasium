# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options
# import pandas as pd
# from bs4 import BeautifulSoup 
# import time


# def init_browser():
#         chrome_options = Options()
#         chrome_options.add_argument("--no-sandbox ")
#         chrome_options.add_argument("--disable-dev-shm-usage")
#         driver_path = 'F:\\DCI-CLASSES\\Python_Classes\\notes_pdf\\Markus\\oop\\extra_helpful\\ComicBot\\modules\\chromedriver.exe'
#         # self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#         # Setup the Chrome driver
#         service = Service(executable_path=driver_path)
#         driver = webdriver.Chrome(service=service)
#         return driver

# def accept_cookies(driver):
#     try:
#         # Wait for the accept cookies button and click it
#         accept_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Accept all")]'))
#         )
#         accept_button.click()
#         print("Accepted cookies.")
#     except Exception as e:
#         print(f"No cookies button found or error occurred: {e}")


# def search_schools(driver , search_query ='Gymnasium Berlin'):
    
#     driver.get(f"https://www.google.com/search?q={search_query}")
    
#     time.sleep(3)
#     # accept_cookies(driver)  # Accept cookies if prompted
#     soup = BeautifulSoup(driver.page_source,'html.parser' )
#     schools =[]
#     for result in soup.find_all('div',class_='tF2Cxc'):
#         try:
#             school_name = result.find('h3').text if result.find('h3') else "N/A"
#             website = result.find('a')['href'] if result.find('a') else "N/A"
#             rank = result.find('cite').text if result.find('cite') else "N/A"
#             description = result.find('span', class_='aCOpRe').text if result.find('span', class_='aCOpRe') else "N/A"
#             schools.append({
#                 'Name': school_name,
#                 'Website': website,
#                 'Rank': rank,
#                 'Description': description
#             })
#         except Exception as e:
#             print(f"Error parsing result: {e}")

#     return schools    



# def save_to_schools(schools):
#     df = pd.DataFrame(schools)
#     df.to_excel('gymnasium_schools_berlin.xlsx', index=False)
#     print("Data saved to gymnasium_schools_berlin.xlsx")
    
    
    
# def main():
#     driver = init_browser()
    
#     # Search for Gymnasium schools in Berlin
#     schools = search_schools(driver, search_query="Gymnasium Berlin")
    
#     # Save the results to an Excel file
#     save_to_schools(schools)
    
#     driver.quit()

# if __name__ == "__main__":
#     main()    
    
    
    
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import pandas as pd
import time

# Setup Selenium and Browser
def init_browser():
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox ")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver_path = 'F:\\DCI-CLASSES\\Python_Classes\\notes_pdf\\Markus\\oop\\extra_helpful\\ComicBot\\modules\\chromedriver.exe'
        # self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        # Setup the Chrome driver
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service)
        return driver
# Handle Google's cookie consent popup
def accept_cookies(driver):
    try:
        # Wait for the accept cookies button and click it
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="L2AGLb"]/div'))
        )
        accept_button.click()
        print("Accepted cookies.")
    except Exception as e:
        print(f"No cookies button found or error occurred: {e}")

# Function to search and extract school data
def search_schools(driver, search_query="Top Gymnasium schools Berlin"):
    # Open the search page
    driver.get(f"https://www.google.com/search?q={search_query}")

    # Wait for page to load and handle cookies
    time.sleep(3)
    accept_cookies(driver)  # Accept cookies if prompted

    # Parse the page content
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    schools = []
    count = 0
    
    # Extract school names, website URLs, and other details
    for result in soup.find_all('div', class_='tF2Cxc'):
        if count >= 20:  # Limit to the top 20 results
            break
        try:
            school_name = result.find('h3').text if result.find('h3') else "N/A"
            website = result.find('a')['href'] if result.find('a') else "N/A"
            rank = result.find('cite').text if result.find('cite') else "N/A"
            description = result.find('span', class_='aCOpRe').text if result.find('span', class_='aCOpRe') else "N/A"
            print(school_name)
            # Only consider results with 'Gymnasium' in the title or description
            # if 'Gymnasium' in school_name or 'Gymnasium' in description:
            schools.append({
                    'Name': school_name,
                    'Website': website,
                    'Rank': rank,
                    'Open Free Day': description
                })
            count += 1

        except Exception as e:
            print(f"Error parsing result: {e}")

    return schools

# Save the results to an Excel sheet
def save_to_excel(schools):
    df = pd.DataFrame(schools)
    df.to_excel('gymnasium_schools_berlin.xlsx', index=False)
    print("Data saved to gymnasium_schools_berlin.xlsx")

# Main function
def main():
    driver = init_browser()
    
    # Search for Gymnasium schools in Berlin
    schools = search_schools(driver, search_query="Top 20 Gymnasium schools in Berlin with website and open free day")
    
    # Save the results to an Excel file
    save_to_excel(schools)
    
    driver.quit()

if __name__ == "__main__":
    main()
    