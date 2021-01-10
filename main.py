from internet_speed_twitter_bot import InternetSpeedTwitterBot
import time

PROMISED_UP = 10
PROMISED_DOWN = 150

internet_speed_twitter_bot = InternetSpeedTwitterBot(PROMISED_UP, PROMISED_DOWN)
internet_speed = internet_speed_twitter_bot.get_internet_speed()
internet_speed_twitter_bot.tweet_at_provider()
time.sleep(10)  # To allow you to see the tweet
internet_speed_twitter_bot.close_driver()

