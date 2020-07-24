# Copyright 2020 Adam Sigal
# Written by Adam Sigal <adamsigal at gmail dot com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from compiler import Compiler
import utils
from vid_info import VidInfo

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
    id="xCLTw1L-H5g"
    )
    response = request.execute()
    print(response['items'][0]['snippet']['channelTitle'])
    title = response['items'][0]['snippet']['title']
    duration_str = response['items'][0]['contentDetails']['duration']
    duration_timedelta = isodate.parse_duration(duration_str)

def download_test(main_dir, title, url):
    vid = YouTube(url)
    streams = vid.streams.filter(progressive=True)
    streams.get_highest_resolution().download(main_dir + '/tmp', title)

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
        ('PnMfNyu7UIw', 'https://www.youtube.com/embed/PnMfNyu7UIw?end=32&start=2'),
        (None, 'http://www.stackoverflow.com')
    ]

    for (id, url) in test_urls:
        try:
            print("id: " + id)
            print("get_id: " + utils.get_id(url))
            if id == utils.get_id(url):
                print("same")
                #print("IDs are same: " + id + " " + get_id(url))
            else:
                print("different")
                #print("IDs are different: " + id + " " + get_id(url))
            print()
        except:
            print("An error occured. id: %s, url: %s. \nContinuing..." % (id, url))
            continue

def start_end_test():
    test_urls = [
        ((0, None), 'http://youtube.com/watch?v=iwGFalTRHDA'),
        ((0, None), 'http://www.youtube.com/watch?v=iwGFalTRHDA&feature=related'),
        ((0, None), 'https://youtube.com/iwGFalTRHDA'),
        ((0, None), 'http://youtu.be/n17B_uFF4cA'),
        ((0, None), 'youtube.com/iwGFalTRHDA'),
        ((0, None), 'youtube.com/n17B_uFF4cA'),
        ((0, None), 'http://www.youtube.com/embed/watch?feature=player_embedded&v=r5nB9u4jjy4'),
        ((0, None), 'http://www.youtube.com/watch?v=t-ZRX8984sc'),
        ((0, None), 'http://youtu.be/t-ZRX8984sc'),
        ((2, 32), 'https://www.youtube.com/embed/PnMfNyu7UIw?end=32&start=2'),
        ((3655, None), 'https://www.youtube.com/watch?v=LCTYRqW-ne8&feature=youtu.be&t=1h55s'),
        ((3600, None), 'https://www.youtube.com/watch?v=LCTYRqW-ne8&feature=youtu.be&t=1h55'),
        ((3340, None), 'https://youtu.be/LCTYRqW-ne8?t=3340')
    ]
    for ((start, end), url) in test_urls:
        try:
            # print("start, end: (" + str(start) + ", " + str(end) + ")")
            # print("url: " + url)

            got_start, got_end = utils.get_start_end(url)

            # print("get_start_end(): (" + str(got_start) + ", " + str(got_end) + ")")

            assert start == got_start
            assert end == got_end
        # if start == got_start and end == got_end:
        #     print("same")
        #     #print("IDs are same: " + id + " " + get_id(url))
        # else:
        #     print("different")
        #     #print("IDs are different: " + id + " " + get_id(url))
        # print()
        except:
            print("An error occured. start: %s, end: %s, url: %s. \nContinuing..." % (got_start, got_end, url))
            continue

    print("All timestamp tests passed")
