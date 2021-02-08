import json
import csv
import os
import tweepy
import ssl
from tqdm import tqdm

TWEET_PATH = "TweetScraper/Data/tweet"
USER_PATH = "TweetScraper/Data/user"
OUTPUT_FILE = "result.json"

tweet_data = os.listdir(TWEET_PATH)
user_data = os.listdir(USER_PATH)

ssl._create_default_https_context = ssl._create_unverified_context

# Oauth keys
consumer_key = "XXX"
consumer_secret = "XXX"
access_token = "XXX"
access_token_secret = "XXX"

# Authentication with Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True, retry_errors=set([401, 404, 500, 502, 503, 504]))

results = {}

for tweet_file in tqdm(tweet_data):
    tweet = open("{}/{}".format(TWEET_PATH,tweet_file))
    tweet = json.load(tweet)
    _id = tweet["id_"]
    if _id == tweet["raw_data"]["conversation_id_str"]:

        user_id = tweet["raw_data"]["user_id_str"]
        if user_id in user_data:
            user_info = open("{}/{}".format(USER_PATH,user_id))
            user_info = json.load(user_info)
            user_name = user_info["raw_data"]["name"]
            user_screen_name = user_info["raw_data"]["screen_name"]
            user_location = user_info["raw_data"]["location"]
            user_description = user_info["raw_data"]["description"]
            user_followers_count = user_info["raw_data"]["followers_count"]
            user_following_count = user_info["raw_data"]["friends_count"]
            user_create_at = user_info["raw_data"]["created_at"]
            user_profile_image = user_info["raw_data"]["profile_image_url"]
            replies = []
            for t in tweepy.Cursor(api.search,q="to: "+user_screen_name, result_type="recent", timeout=999999).items():
            #for t in tweepy.Cursor(api.user_timeline, screen_name=user_screen_name,timeout=999999).pages():
                if hasattr(t, "in_reply_to_status_id_str"):
                    if (t.in_reply_to_status_id_str==_id):
                        replies.append({"reply_user":t.user.screen_name, "reply_text":t.text.replace("\n", " ")})
        else:
            user_name = ""
            user_name = ""
            user_screen_name = ""
            user_location = ""
            user_description = ""
            user_followers_count = ""
            user_following_count = ""
            user_create_at = ""
            user_profile_image = ""
        tweet_keys = list(tweet["raw_data"]["entities"].keys())
        tweet_url = "https://twitter.com/{}/status/{}".format(user_screen_name,_id)
        tweet_text = tweet["raw_data"]["full_text"]
        tweet_time = tweet["raw_data"]["created_at"]
        num_of_likes = tweet["raw_data"]["favorite_count"]
        num_of_retweet = tweet["raw_data"]["retweet_count"]
        num_of_reply = len(replies)
        mentions = [ i["screen_name"] for i in tweet["raw_data"]["entities"]["user_mentions"]]
        num_of_mentions = len(mentions)
        hashtags = [ i["text"] for i in tweet["raw_data"]["entities"]["hashtags"]]
        num_of_hashtags = len(hashtags)
        if "media" in tweet_keys:
            img_url = [ i["media_url"] for i in tweet["raw_data"]["entities"]["media"]]
        else:
            img_url = None
        results[_id] = {"text": tweet_text, "url": tweet_url, "time": tweet_time, "num_of_likes": num_of_likes, "num_of_retweet": num_of_retweet, "num_of_reply": num_of_reply, "mentions": mentions, "num_of_mentions": num_of_mentions, "hashtags": hashtags, "num_of_hashtags": num_of_hashtags, "img_url": img_url, "reply": replies, "user_info":{
            "user_name": user_name, "screen_name": user_screen_name, "location": user_location, "description": user_description, "followers_count": user_followers_count, "following_count": user_following_count, "creat_time": user_create_at, "profile_image": user_profile_image
            }
            }


with open(OUTPUT_FILE, "w") as json_file:
    json.dump(results, json_file, ensure_ascii=False, indent=4)
    print("Done")
