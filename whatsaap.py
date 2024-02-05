import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

error_list = list()

# Write the file absolute path which you want to send in media. Can be image , video, pdf
image_path = "/Users/satyamb/PycharmProjects/whatsaapMessageAutomator/save_the_date_reception.jpg"

# Wiite the message in message.json if you want to send a text message.
json_file_path = 'message.json'


def get_message():
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data["message"]


def login_whatsapp():
    # Start the Safari browser
    driver = webdriver.Safari()

    # Open WhatsApp Web
    driver.get("https://web.whatsapp.com/")

    # Wait for the user to scan the QR code
    wait = WebDriverWait(driver, 600)  # Adjust the timeout as needed
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_2QgSC')))

    return driver


def send_whatsaap_messagess(driver, phone_number, name, message):
    search_box = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
    i = 0
    while i < 12:
        search_box.send_keys(Keys.BACKSPACE)
        i = i + 1
    search_box.send_keys(phone_number)
    search_box.send_keys(Keys.ENTER)
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[4]')))
        time.sleep(2)

        input_box = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div')
        input_box.send_keys(f"Hello {name}, \n {message}")

        time.sleep(1)
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)
        print(f"Message sent to {name} with phone number {phone_number}")

    except Exception as e:
        print(e)
        error_list.append(name)


def send_whatsapp_media(driver, phone_number, name):
    search_box = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
    i = 0
    while i < 12:
        search_box.send_keys(Keys.BACKSPACE)
        i = i + 1
    search_box.send_keys(Keys.ENTER)
    search_box.send_keys(phone_number)
    search_box.send_keys(Keys.ENTER)
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[4]')))
        time.sleep(4)

        plus_button = driver.find_element(By.XPATH,
                                          '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div')
        plus_button.click()

        # Locate and click the "Photo and Video" option
        photo_video_option = driver.find_element(By.XPATH,
                                                 '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/ul/div/div[2]/li/div/input')
        photo_video_option.send_keys(image_path)

        input_box = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div')
        time.sleep(1)
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        print(f"Message sent to {name} with phone number {phone_number}")
    except Exception as e:
        print(e)
        error_list.append(name)


def main():
    # Write your message in the message.json
    message = get_message()

    # Log into WhatsApp Web
    whatsapp_driver = login_whatsapp()
    print("Login complete")
    try:
        # Read contacts from the CSV file - Write the file name here.
        with open('Smritu Marriage  - Reception List.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row if present
            for row in reader:
                name, phone_number = row[1:3]

                # Select Either function media to send photos, videos, pdfs, etc. Or select message function to send plain message
                send_whatsapp_media(whatsapp_driver, phone_number, name)
                # send_whatsaap_messagess(whatsapp_driver, phone_number, name, message)
    finally:
        print(error_list)
        whatsapp_driver.quit()


if __name__ == "__main__":
    main()
