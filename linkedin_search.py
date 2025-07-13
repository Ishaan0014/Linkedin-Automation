from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import credentials  # LinkedIn credentials file

# 🔍 Setup Logging
logging.basicConfig(filename='linkedin_bot.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# 🔍 Step 1: Get Search Input from User
search_query = input("🔍 Enter the keyword to search on LinkedIn: ")

# 🤝 Step 2: Get Number of Connection Requests from User
while True:
    try:
        total_requests = int(input("🤝 Enter the number of connection requests you want to send: "))
        if total_requests > 0:
            break
        else:
            print("⚠️ Please enter a positive number.")
    except ValueError:
        print("❌ Invalid input. Please enter a valid number.")

# 🔐 Step 3: Load Credentials
email = credentials.EMAIL
password = credentials.PASSWORD

# 🌐 Step 4: Setup WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)  # Keep browser open
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

# 🔗 Step 5: Open LinkedIn Login Page
driver.get("https://www.linkedin.com/login")

# 🔑 Step 6: Login with Stored Credentials
wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(email)
driver.find_element(By.ID, "password").send_keys(password)
driver.find_element(By.XPATH, "//button[@type='submit']").click()

# 🔎 Step 7: Automatically Search
try:
    search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Search')]")))
    search_box.send_keys(search_query)
    time.sleep(2)
    search_box.send_keys(Keys.RETURN)
    wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label, 'Invite')]")))
    logging.info(f"Search completed for '{search_query}'.")
    
    # Click on 'See all people results'
    try:
        see_all_people = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'See all people results')]")))
        see_all_people.click()
        logging.info("Clicked on 'See all people results'.")
        time.sleep(5)
    except Exception as e:
        logging.warning(f"Could not click on 'See all people results': {e}")

except Exception as e:
    logging.error(f"Error during search: {e}")

# 🤝 Step 8: Send Connection Requests
sent_requests = 0  # Counter for sent requests

def scroll_page():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

while sent_requests < total_requests:
    try:
        time.sleep(5)  # Allow page to load
        scroll_page()

        # 🖱️ Find all visible and enabled Connect buttons
        connect_buttons = [
            btn for btn in driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Invite')]")
            if btn.is_displayed() and btn.is_enabled()
        ]

        if not connect_buttons:
            logging.warning("No more connect buttons found on this page.")

        for button in connect_buttons:
            if sent_requests >= total_requests:
                break
            try:
                button.click()
                time.sleep(2)
                
                # ✅ Handle "Add a Note" Popup
                try:
                    send_without_note_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Send without a note')]"))
                    )
                    driver.execute_script("arguments[0].click();", send_without_note_button)
                    logging.info(f"✅ Connection request {sent_requests + 1} sent successfully!")
                    sent_requests += 1
                except:
                    logging.warning("No 'Add Note' popup detected, request sent directly.")
                    sent_requests += 1
                
                time.sleep(2)
            except Exception as e:
                logging.error(f"Skipping profile due to error: {e}")

        # 🔄 Move to next page if requests not completed
        if sent_requests < total_requests:
            try:
                next_page = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Next')] | //span[contains(@aria-label, 'Next')]")
                driver.execute_script("arguments[0].click();", next_page)
                logging.info("📄 Moving to the next page...")
                time.sleep(5)
            except:
                logging.error("No more pages available. Stopping process.")
                break
    except Exception as e:
        logging.error(f"Error while sending requests: {e}")
        break

# 🚪 Step 9: Keep Browser Open
logging.info("🌍 Keeping browser open for manual interaction...")
input("🔴 Press ENTER to close the browser...")
driver.quit()
