from selenium import webdriver
import time
import os

chrome_driver_path = r'chromedriver.exe'

TWITTER_PWD = os.environ["TWITTER_PWD"]
TWITTER_USERNAME = os.environ["TWITTER_USERNAME"]
TWITTER_EMAIL = os.environ["TWITTER_EMAIL"]

class InternetSpeedTwitterBot():
    def __init__(self, promised_up, promised_down):
        self.driver = webdriver.Chrome(executable_path=chrome_driver_path)
        self.promised_up = promised_up
        self.promised_down = promised_down
        self.twitter_pwd = TWITTER_PWD
        self.twitter_username = TWITTER_USERNAME
        self.twitter_email = TWITTER_EMAIL
        self.twitter_url = "https://www.twitter.com"
        self.speed_test_url = "https://www.speedtest.net/"
        self.download_number = 0
        self.upload_number = 0
        self.internet_speed = [self.download_number, self.upload_number]

    def get_internet_speed(self):
        """Returns a list object containing download and upload speeds"""
        self.driver.get(self.speed_test_url)
        # Handle Cookies Pop-up
        try:
            consent_button = self.driver.find_element_by_xpath("//*[@aria-label='I Consent']")
            consent_button.click()
        except:
            pass
        speed_test_button = self.driver.find_element_by_xpath("//*[@aria-label='start speed test - connection type multi']")
        speed_test_button.click()
        stats_available = False
        # Loop until stats are available
        while not stats_available:
            time.sleep(20) #Wait for speed test to complete
            try:
                self.download_number = float(self.driver.find_element_by_class_name("download-speed").text)
                self.upload_number = float(self.driver.find_element_by_class_name("upload-speed").text)
                stats_available = True
            except:
                pass
            finally:
                pass
        self.internet_speed = [self.download_number, self.upload_number]
        return self.internet_speed


    def tweet_at_provider(self):
        self.driver.get(self.twitter_url)
        time.sleep(5)
        # Login to Twitter
        self.login_to_twitter()
        time.sleep(5)
        # Send Tweet
        self.send_tweet()

    def close_driver(self):
        self.driver.quit()

    def login_to_twitter(self):
        try:
            # If prompted with login button initially
            self.login_button = self.driver.find_element_by_xpath("//*[@data-testid='loginButton']")
            self.login_button.click()
        except:
            pass
        finally:
            self.username_input = self.driver.find_element_by_name("session[username_or_email]")
            self.username_input.send_keys(self.twitter_email)
            self.password_input = self.driver.find_element_by_name("session[password]")
            self.password_input.send_keys(self.twitter_pwd)
            self.login_button = self.driver.find_element_by_xpath("//*[@data-testid='LoginForm_Login_Button']")
            self.login_button.click()

    def send_tweet(self):
        self.textbox_input = self.driver.find_element_by_xpath("//*[@data-testid='tweetTextarea_0']")
        tweet_text = f"Hey Internet Provider, why is my internet speed {self.download_number} down/{self.upload_number} up when I pay for {self.promised_down} down/{self.promised_up} up?"
        self.textbox_input.send_keys(tweet_text)
        self.tweet_button = self.driver.find_element_by_xpath("//*[@data-testid='tweetButtonInline']")
        self.tweet_button.click()