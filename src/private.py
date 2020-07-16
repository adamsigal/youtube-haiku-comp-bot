import praw
from apiclient.discovery import build

def get_yt():
    return build('youtube', 'v3', developerKey='AIzaSyDdkPJNXR6_ZoifmGWGTxknxpOjmOHmxgA')

def get_reddit():
    return praw.Reddit(client_id="3ad_76DYm9V_8w",
                       client_secret="_SfshD61Ht7L31b2y2FPSNkq-DY",
                       user_agent="my user agent")
