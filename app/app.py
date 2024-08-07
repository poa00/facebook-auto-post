# -*- coding: utf-8 -*-
import json, sqlite3, pyautogui, sys, os
from configparser import ConfigParser
from time import sleep

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

MAIN_URL = "https://www.facebook.com/"
MARKETPLACE_URL = "https://www.facebook.com/marketplace/create/item"

class App:
    def __init__(self, email="", password="", language="en", path="C:/Users/%USERPROFILE%/Pictures", time_to_sleep="0.7", browser="Chrome"):
        self.email = email
        self.password = password
        self.path = path
        self.browser = browser
        self.language = language
        self.marketplace_options = None
        self.posts = None
        self.time_to_sleep = float(time_to_sleep)
        self.emojis_available = False
        with open(self.resource_path('marketplace_options.json'), encoding='utf-8') as f:
            self.marketplace_options = json.load(f)
            self.marketplace_options = self.marketplace_options[self.language]
        # To remove the pop up notification window
        if browser == "Firefox":
            self.emojis_available = True
            options = FirefoxOptions()
            options.set_preference("dom.webnotifications.enabled", False)
            self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        else:
            self.emojis_available = False
            options = ChromeOptions()
            options.add_argument("--disable-notifications")
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)

        self.driver.maximize_window()
        self.main_url = MAIN_URL
        self.marketplace_url = MARKETPLACE_URL
        self.driver.get(self.main_url)
        self.log_in()
        self.posts = self.fetch_all_posts()
        for post in self.posts:
            self.move_from_home_to_marketplace_create_item()
            self.create_post(post)
        sleep(2)
        self.driver.quit()

    def log_in(self):
        email_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "email")))
        email_input.send_keys(self.email)
        password_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "pass")))
        password_input.send_keys(self.password)
        login_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@type='submit']")))
        login_button.click()


    def move_from_home_to_marketplace_create_item(self):
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//a[@aria-label="Facebook"]')))
        self.driver.get(self.marketplace_url)


    def add_photos_to_post(self, post_folder):
        if self.language == "es":
            # Latinoamerica
            photo_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="' + self.marketplace_options["labels"]["Marketplace"] + '"]/div/div[3]/div[2]/div/div[@role="button"]')))
        else:
            # English version - New version of facebook with photo and video buttons
            photo_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="' + self.marketplace_options["labels"]["Marketplace"] + '"]/div/div[3]/div[1]/div/div/div[1]')))
        photo_button.click()
        pyautogui.sleep(2)
        pyautogui.hotkey('ctrl', 'l', interval=0.5)
        pyautogui.sleep(self.time_to_sleep)
        pyautogui.write(self.path + post_folder)
        pyautogui.sleep(self.time_to_sleep)
        pyautogui.press('enter')
        pyautogui.sleep(2)
        pyautogui.press('tab')
        pyautogui.sleep(self.time_to_sleep)
        pyautogui.press('tab')
        pyautogui.sleep(self.time_to_sleep)
        pyautogui.press('tab')
        pyautogui.sleep(self.time_to_sleep)
        pyautogui.press('tab')
        pyautogui.sleep(2)
        pyautogui.hotkey('ctrl', 'a', interval=0.5)
        pyautogui.sleep(self.time_to_sleep)
        pyautogui.press('enter')
        pyautogui.sleep(self.time_to_sleep)

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def add_text_to_post(self, title, price, description, label):
        title_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//label[@aria-label='" + self.marketplace_options["labels"]["Title"] + "']/input")))
        title_input.send_keys(title)
        price_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//label[@aria-label='" + self.marketplace_options["labels"]["Price"] +  "']/input")))
        price_input.send_keys(price)
        # More Details
        if self.language == "es":
            # Latinoamerica
            more_details_button = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="' + self.marketplace_options["labels"]["Marketplace"] + '"]/div/div[9]/div/div/div/div[@role="button"]')))
            more_details_button.click()
        else:
            # English version - New version of facebook with different position of more details button
            more_details_button = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="' + self.marketplace_options["labels"]["Marketplace"] + '"]/div/div[11]/div/div/div/div[@role="button"]')))
            more_details_button.click()
        description_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//label[@aria-label='" + self.marketplace_options["labels"]["Description"] +  "']/div/textarea")))
        description_input.send_keys(description.replace("\r\n", "\n"))
        if label:
            label_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//label[@aria-label='" + self.marketplace_options["labels"]["Product Labels"] + "']/div/div[2]/div/textarea")))
            # To add the last label, you need to add a comma
            if not label.endswith(","):
                label += ","
            label_input.send_keys(label)


    def fetch_all_posts(self):
        posts = None
        try:
            sqliteConnection = sqlite3.connect('articles.db')
            cursor = sqliteConnection.cursor()
            sqlite_select_query = """SELECT * from item"""
            cursor.execute(sqlite_select_query)
            posts = cursor.fetchall()
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)

        finally:
            if (sqliteConnection):
                sqliteConnection.close()

        return posts


    def clean_characters_bmp(self, text):
        return ''.join(c for c in text if ord(c) <= 0xFFFF).strip()


    def create_post(self, post):
        self.add_photos_to_post(post[8])
        if not self.emojis_available:
            self.add_text_to_post(self.clean_characters_bmp(post[1]), post[2], self.clean_characters_bmp(post[7]), post[10])
        else:
            self.add_text_to_post(post[1], post[2], post[7], post[10])

        category_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//label[@aria-label='" + self.marketplace_options["labels"]["Category"] +  "']")))
        category_input.click()
        sleep(self.time_to_sleep)
        category_option = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']/div/div/div/span/div/div[" + self.get_element_position("categories", post[3]) + "]")))
        category_option.click()
        sleep(self.time_to_sleep)

        state_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//label[@aria-label='" + self.marketplace_options["labels"]["State"] +  "']")))
        state_input.click()
        sleep(self.time_to_sleep)
        state_option = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@role="listbox"]/div/div/div/div/div[1]/div/div[' + self.get_element_position("states", post[4]) + ']')))
        state_option.click()
        sleep(self.time_to_sleep)

        if post[5] == "platforms":
            type_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//label[@aria-label='" + self.marketplace_options["labels"]["Platform"] +  "']")))
            type_input.click()
            sleep(self.time_to_sleep)
            type_option = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@role="menu"]/div/div/div[1]/div/div[' + self.get_element_position("platforms", post[6]) + ']')))
            type_option.click()
            sleep(self.time_to_sleep)

        if post[5] == "devices":
            type_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//label[@aria-label='" + self.marketplace_options["labels"]["Device Name"] +  "']")))
            type_input.click()
            sleep(self.time_to_sleep)
            type_option = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@role="menu"]/div/div/div[1]/div/div[' + self.get_element_position("devices", post[6]) + ']')))
            type_option.click()
            sleep(self.time_to_sleep)

        next_button = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='" + self.marketplace_options["labels"]["Next Button"] +  "']")))
        next_button.click()

        self.post_in_more_places(post[9])
        sleep(self.time_to_sleep)
        
        post_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='" + self.marketplace_options["labels"]["Post"] +  "']")))
        post_button.click()
        sleep(self.time_to_sleep)


    def get_element_position(self, key, specific):
        if specific in self.marketplace_options[key]:
            return str(self.marketplace_options[key][specific])
        return -1


    def post_in_more_places(self, groups):
        groups_positions = groups.split(",")

        for group_position in groups_positions:
            group_input = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='" + self.marketplace_options["labels"]["Marketplace"] +  "']/div/div/div/div[4]/div/div/div/div/div/div/div[2]/div[" + group_position + "]")))
            group_input.click()
            sleep(self.time_to_sleep)


if __name__ == '__main__':
    config_object = ConfigParser()
    config_object.read("config.ini")
    facebook = config_object["FACEBOOK"]
    configuration = config_object["CONFIG"]
    app = App(facebook["email"], facebook["password"], configuration["language"], configuration["images_path"], configuration["time_to_sleep"], configuration["browser"])