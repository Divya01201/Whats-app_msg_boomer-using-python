from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ----- Chrome options -----
options = webdriver.ChromeOptions()
# Yeh line ensure karegi ki aapka login (QR scan) ek hi baar ho aur baar-baar na karna pade
options.add_argument(r"user-data-dir=C:\WhatsAppProfile")

# ----- Configuration -----
WHATSAPP_URL = "https://web.whatsapp.com/"
TARGET_NAME = "Chachi"
MESSAGE_TEXT = "Message sent using Python!!!"
MESSAGE_COUNT = 10
DELAY_BETWEEN_MESSAGES = 1

# ----- Launch Chrome -----
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(WHATSAPP_URL)

# Wait for QR scan / page load (2 minutes)
wait = WebDriverWait(driver, 180)

try:
    # Locate chat by name
    chat_xpath = f'//span[contains(@title,"{TARGET_NAME}")]'
    chat_title = wait.until(EC.presence_of_element_located((By.XPATH, chat_xpath)))
    chat_title.click()
    print(f"Opened chat: {TARGET_NAME}")

    # Locate input box (WhatsApp ke liye sabse stable selector)
 #input_xpath = '//div[@contenteditable="true"]'
    input_xpath = '//footer//div[@contenteditable="true"]'
    input_box = wait.until(EC.presence_of_element_located((By.XPATH, input_xpath)))
    print("Message input box found.")

    # Send messages
    for i in range(MESSAGE_COUNT):
        input_box.send_keys(MESSAGE_TEXT)
        input_box.send_keys(Keys.ENTER)
        print(f"Sent message {i + 1}/{MESSAGE_COUNT}")
        time.sleep(DELAY_BETWEEN_MESSAGES)

except TimeoutException:
    print("❌ Error: Chat or input box not found. Check login and target name.")
except NoSuchElementException:
    print("❌ Error: Element not found on the page.")
finally:
    print("✅ Task completed. Closing browser in 5 seconds...")
    time.sleep(5)
    driver.quit()
