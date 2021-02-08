# Twitter-data-crawler

## Usage
Step1. 使用TweetScraper 爬取資料
[Reference](https://github.com/jonbakerfish/TweetScraper)

Step2. 使用data_cleaner.py 整理資料並爬取reply

(爬取reply的code為參照 [Reference](https://hackernoon.com/scraping-tweet-replies-with-python-and-tweepy-twitter-api-a-step-by-step-guide-z11x3yr8))


## Requirement
```
scrapy
scrapy-selenium
ipython
ipdb
tqdm
tweepy
```

## Data

### Tweet
* tweet_id
* text
* url
* time
* num_of_likes
* num_of_retweet
* num_of_reply
* mentions
* num_of_mentions
* hashtags
* num_of_hashtags
* img_url
* reply
### User_info
* user_name
* screen_name
* location
* description
* followers_count
* following_count
* creat_time
* profile_image
