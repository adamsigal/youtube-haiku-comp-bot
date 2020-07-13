# By Adam Sigal
from compiler import Compiler

import os
import praw
from apiclient.discovery import build
import datetime
import isodate
import re
from urllib.parse import urlparse, parse_qs
import math
from pytube import YouTube
from moviepy.editor import *
from moviepy.video.tools.segmenting import findObjects
import pygame
import time
import random

def yt_request_test(compiler):
    request = compiler.youtube.videos().list(
    part="snippet,contentDetails",
    id="Ks-_Mh1QhMc"
    )
    response = request.execute()
    print(response['items'][0]['snippet']['channelTitle'])
    title = response['items'][0]['snippet']['title']
    duration_str = response['items'][0]['contentDetails']['duration']
    duration_timedelta = isodate.parse_duration(duration_str)


def get_submission_list_test(compiler, period="week", max_vids=5):
    submission_list, total_duration, description = compiler.get_submission_list(period=period, max_vids=max_vids)
    for i in range(0, 10):
        print(submission_list[i].title)
        print(description[i] + "\n")

def yt_id_tests():
    test_urls = [
        ('iwGFalTRHDA', 'http://youtube.com/watch?v=iwGFalTRHDA'),
        ('iwGFalTRHDA', 'http://www.youtube.com/watch?v=iwGFalTRHDA&feature=related'),
        ('iwGFalTRHDA', 'https://youtube.com/iwGFalTRHDA'),
        ('n17B_uFF4cA', 'http://youtu.be/n17B_uFF4cA'),
        ('iwGFalTRHDA', 'youtube.com/iwGFalTRHDA'),
        ('n17B_uFF4cA', 'youtube.com/n17B_uFF4cA'),
        ('r5nB9u4jjy4', 'http://www.youtube.com/embed/watch?feature=player_embedded&v=r5nB9u4jjy4'),
        ('t-ZRX8984sc', 'http://www.youtube.com/watch?v=t-ZRX8984sc'),
        ('t-ZRX8984sc', 'http://youtu.be/t-ZRX8984sc'),
        (None, 'http://www.stackoverflow.com')
    ]

    for (id, url) in test_urls:
        try:
            print("id: " + id)
            print("get_id: " + get_id(url))
            if id == get_id(url):
                print("same")
                #print("IDs are same: " + id + " " + get_id(url))
            else:
                print("different")
                #print("IDs are different: " + id + " " + get_id(url))
            print()
        except:
            print("An error occured. id: %s, url: %s. \nContinuing..." % (id, url))
            continue
