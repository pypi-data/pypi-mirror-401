#pip install selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import StaleElementReferenceException
import time

#pip install chromedriver-py
from webdriver_manager.chrome import ChromeDriverManager
from os import getcwd

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
#chrome_options.add_argument("--headless=new")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

website = f"{getcwd()}\\index.html"

driver.get(website)

rec_file = f"{getcwd()}\\input.txt"

def listen():
    try:
        # Initial wait for the button and first click
        start_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'startButton')))
        start_button.click()
        print("Listening...")
        
        output_text = ""
        is_second_click = False

        while True:
            try:
                # RE-FIND the elements inside the loop to avoid staleness
                output_element = driver.find_element(By.ID, 'output')
                current_button = driver.find_element(By.ID, 'startButton')
                
                current_text = output_element.text.strip()
                button_text = current_button.text

                # Check button state
                if "Start listening" in button_text and is_second_click:
                    if output_text: 
                        is_second_click = False
                elif "listening..." in button_text:
                    is_second_click = True

                # Check if text has changed
                if current_text != output_text:
                    output_text = current_text
                    # IMPORTANT: Use lowercase "w" for write mode
                    with open(rec_file, "w", encoding="utf-8") as file:
                        file.write(output_text.lower())
                    print("USER : " + output_text)
                
                # Small sleep to prevent high CPU usage
                time.sleep(0.5)

            except StaleElementReferenceException:
                # If the element goes stale (e.g., during a JS update), 
                # just skip this loop and try finding it again in the next iteration.
                continue

    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")


listen()


