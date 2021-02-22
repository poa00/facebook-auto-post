import json
import sqlite3
from configparser import ConfigParser
from time import sleep

import keyboard
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class App:
    def __init__(self, email= "", password= "", 
                 path="", language=""):
        self.email = email
        self.password = password
        self.path = path
        self.language = language
        self.marketplace_options = None
        self.posts = None
        with open('marketplace_options.json', encoding='utf-8') as f:
            self.marketplace_options = json.load(f)
            self.marketplace_options = self.marketplace_options[self.language]
        # To remove the pop up notification window
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome('./chromedriver', options=chrome_options)
        self.main_url = "https://www.facebook.com"
        self.marketplace_url = "https://www.facebook.com/marketplace/create/item"
        self.driver.get(self.main_url)
        self.log_in()
        self.posts = self.fetch_all_posts()
        for post in self.posts:
            self.move_from_home_to_marketplace_create_item()
            self.create_post(post)
        self.driver.quit()
        
        
    def log_in(self):
        try:
            email_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "email")))
            email_input.send_keys(self.email)
            password_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "pass")))
            password_input.send_keys(self.password)
            login_button = self.driver.find_element_by_xpath("//*[@type='submit']")
            login_button.click()
        except Exception:
            print('Some exception occurred while trying to find username or password field')
        

    def move_from_home_to_marketplace_create_item(self):
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//a[@aria-label="Facebook"]')))
            self.driver.get(self.marketplace_url)
        except Exception:
            print('Some exception occurred while trying to find facebook logo')


    def add_photos_to_post(self, post_folder):
        try:
            photo_button = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="' + self.marketplace_options["labels"]["Add Photos"] + '"]')))
            photo_button.click()
            sleep(0.5)
            keyboard.send("ctrl+l")
            keyboard.write(self.path + post_folder)
            keyboard.send("enter")
            sleep(0.5)
            keyboard.send("tab")
            sleep(0.5)
            keyboard.send("tab")
            sleep(0.5)
            keyboard.send("tab")
            sleep(0.5)
            keyboard.send("tab")
            sleep(0.5)
            keyboard.send("ctrl+a")
            sleep(0.5)
            keyboard.send("enter")
        except Exception:
            print('Some exception occurred while trying to find photo button')
    

    def add_text_to_post(self, title, price, description):
        try:
            title_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//label[@aria-label='" + self.marketplace_options["labels"]["Title"] + "']/div/div/input")))
            title_input.send_keys(title)
            price_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//label[@aria-label='" + self.marketplace_options["labels"]["Price"] +  "']/div/div/input")))
            price_input.send_keys(price)
            description_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//label[@aria-label='" + self.marketplace_options["labels"]["Description"] +  "']/div/div/textarea")))
            description_input.send_keys(description)
        except Exception:
            print('Some exception occurred while trying to find input text fields')


    def fetch_all_posts(self):
        posts = None
        try:
            sqliteConnection = sqlite3.connect('articles.db')
            cursor = sqliteConnection.cursor()
            sqlite_select_query = """SELECT * from post"""
            cursor.execute(sqlite_select_query)
            posts = cursor.fetchall()
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)

        finally:
            if (sqliteConnection):
                sqliteConnection.close()

        return posts


    def create_post(self, post):
        self.add_photos_to_post(post[8])
        self.add_text_to_post(post[1], post[2], post[7])

        category_input = self.driver.find_element_by_xpath("//label[@aria-label='" + self.marketplace_options["labels"]["Category"] +  "']")
        category_input.click()
        sleep(0.5)
        category_option = self.driver.find_element_by_xpath("//div[@data-pagelet='root']/div[@role='dialog']/div/div/span/div/div[" + self.get_element_position("categories", post[3]) + "]")
        category_option.click()
        
        state_input = self.driver.find_element_by_xpath("//label[@aria-label='" + self.marketplace_options["labels"]["State"] +  "']")
        state_input.click()
        sleep(0.5)
        state_option = self.driver.find_element_by_xpath('//div[@data-pagelet="root"]/div/div/div/div/div/div[@role="menuitemradio"][' + self.get_element_position("states", post[4]) + ']')
        state_option.click()

        if post[5] == "platforms":
            type_input = self.driver.find_element_by_xpath("//label[@aria-label='" + self.marketplace_options["labels"]["Platform"] +  "']")
            type_input.click()
            sleep(0.5)
            type_option = self.driver.find_element_by_xpath('//div[@data-pagelet="root"]/div[@role="menu"]/div/div/div/div/div[' + self.get_element_position("platforms", post[6]) + ']')
            type_option.click()
        
        if post[5] == "devices":
            type_input = self.driver.find_element_by_xpath("//label[@aria-label='" + self.marketplace_options["labels"]["Device Name"] +  "']")
            type_input.click()
            sleep(0.5)
            type_option = self.driver.find_element_by_xpath('//div[@data-pagelet="root"]/div[@role="menu"]/div/div/div/div/div[' + self.get_element_position("devices", post[6]) + ']')
            type_option.click()

        try:
            next_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='" + self.marketplace_options["labels"]["Next Button"] +  "']")))
            next_button.click()
        except Exception:
            print('Some exception occurred while trying to find next button')
        
        self.post_in_more_places(post[9])


    def get_element_position(self, key, specific):
        if specific in self.marketplace_options[key]:
            return self.marketplace_options[key][specific]
        return -1


    def post_in_more_places(self, groups):
        groups_positions = groups.split(",")

        for group_position in groups_positions:
            group_input = self.driver.find_element_by_xpath("//div[@aria-label='" + self.marketplace_options["labels"]["Marketplace"] +  "']/div/div/div/div[4]/div/div/div/div/div/div/div/div/div/div[2]/div[" + group_position + "]")
            group_input.click()
            sleep(0.5)

        post_button = self.driver.find_element_by_xpath("//div[@aria-label='" + self.marketplace_options["labels"]["Post"] +  "']")
        post_button.click()


if __name__ == '__main__':
    config_object = ConfigParser()
    config_object.read("config.ini")
    facebook_user = config_object["FACEBOOKUSER"]
    configuration = config_object["CONFIG"]
    app = App(facebook_user["email"], facebook_user["password"], configuration["images_path"], configuration["language"])