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
import youtube_dl

class Compiler:
    def __init__(self, youtube, reddit, main_dir):
        self.youtube = youtube
        self.reddit = reddit
        self.main_dir = main_dir


    # Fetches the submissions from reddit along with their info
    def fetch_vid_info(self, period="month", time_limit=datetime.timedelta.max, max_vids=50, min_score=0):
        """
        Args:
            period (str): "week", "month", "year", "all time"
            time_limit (timedelta): time limit for a given compilation
            max_vids (int): max number of vids for a given compilation
            min_score (int): min # of upvotes to get into the compilation
        Returns:
            vid_info (VidInfo[]): each element contains info about video:
                (submission, title, channel, duration, start, end)
            total_duration (timedelta): sum of videos' lengths
        """

        vid_info = []
        total_duration = datetime.timedelta(seconds = 0)
        ctr = 0
        for submission in self.reddit.subreddit("youtubehaiku").top(period):
            if (ctr >= max_vids):
                break
            try:
                vid_id = utils.get_yt_id(submission.url)

                # To make sure that link isn't broken
                request = self.youtube.videos().list(
                    part="ContentDetails, snippet",
                    id=vid_id
                )
                response = request.execute()

                # if 'items' is empty, no vid data was retrievable => don't want in list
                assert len(response['items']) != 0

                # parse url to see if it contains start & end information
                start, end = utils.get_start_end(submission.url)
                start = int(start)
                start_td = datetime.timedelta(seconds = start)
                # `end` will either be returned as None or int of seconds
                if end is not None:
                    end = int(end)
                    duration_timedelta = datetime.timedelta(seconds = end) - start_td
                else:
                    duration_str = response['items'][0]['contentDetails']['duration']
                    duration_timedelta = isodate.parse_duration(duration_str) - start_td

                # if we reach a max duration or min score, we end the for loop
                if (total_duration+duration_timedelta > time_limit) or (submission.score < min_score):
                    break

                title = response['items'][0]['snippet']['title']
                channel = response['items'][0]['snippet']['channelTitle']

                vid_info.append( VidInfo(submission, title, channel, duration_timedelta, start, end) )
                total_duration += duration_timedelta
                ctr += 1

            except Exception as e:
                print("Error with post: ", e)
                print("Post title: '%s'. \nPost url: %s" % (submission.title, submission.url))
                if "quota" in str(e):
                    exit(0)
                print("Continuing...")

        return (vid_info, total_duration)

    # generates a list contaning descriptions of each video
    def gen_description(self, vid_info):
        """
        Args:
            vid_info (VidInfo[]): info from videos to be included in compilation
        Returns:
            description (string[]): list where each element contains string
                corresponding to the description of a single video
        """
        description = []
        total_duration = datetime.timedelta(seconds = 0)
        for i in range(len(vid_info)):
            description.append(str(total_duration) + ' "' + vid_info[i].title + '" - ' + vid_info[i].channel + "\n" + vid_info[i].submission.url)
            total_duration += vid_info[i].duration

        return description

    # writes description to file
    def write_description(self, comp_name, description):
        """
        Args:
            comp_name (string): name of the compilation
            description (string[]): list of individual video descriptions
        """
        str_description = "\n\n".join(description)

        # hashtags from video titles get automatically added to the
        # compilation's hastags, so I just remove them
        str_description = str_description.replace('#', ' ')
        str_description = "Best posts from https://www.reddit.com/r/youtubehaiku/ \n\nVideos:\n" + str_description

        f = open(self.main_dir + "/final/" + comp_name + "_description" , "w")
        f.write(str_description)
        f.close()
        print("Description written to file: " + self.main_dir + "/final/" + comp_name + "_description")


    # Generates name of the compilation based on date and number of videos
    def comp_name_gen(self, period, num_vids):
        if period in ('day', 'week', 'month', 'year'):
            return str(datetime.datetime.date(datetime.datetime.now())) + "_top_" + str(num_vids) + "_of_" + period
        else:
            raise Exception("invalid period argument, must be one of: 'day', 'week', 'month', 'year'")


    def download_vids(self, vid_info, delete_past_vids=True):
        # use yt-dl. if False, use pytube
        yt_dl = True
        if delete_past_vids:
            os.system("rm " + self.main_dir + "/vids/*")

        # for having consistent naming of downloaded video files
        l = len(vid_info)
        decimal_places = math.ceil(math.log10(l))
        format_string = "{:0" + str(decimal_places) + "d}"

        for i in range(l):
            #utils.printProgressBar(i+1, l, prefix = 'Downloading videos:', suffix = 'Complete', length = 50)

            vid_name = format_string.format(i+1) + "-" + vid_info[i].submission.title.replace(" ", "_")

            if yt_dl:
                # # quotation marks must be escaped for terminal commands
                #vid_name = vid_name.replace("'", "\\'").replace('"', '\\"')
                #vid_name = re.escape(vid_name)
                vid_name = vid_name.translate(str.maketrans({'"':  r'\\"',
                                                             "'":  r"\\'",
                                                             "%": r"percent"}))
                                    # even when escaped, % sign messes up yt-dl
                print("downloading: " + vid_name)
                #
                # os.system("youtube-dl " + vid_info[i].submission.url + " -o" + self.main_dir + "/vids/" + vid_name)

                ydl_opts = {
                    'outtmpl': self.main_dir + "/vids/" + vid_name,
                    'cookiefile': self.main_dir + "/private/" + "cookies.txt"
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([vid_info[i].submission.url])
            else:
                vid = YouTube(vid_info[i].submission.url)
                streams = vid.streams.filter(progressive=True)
                streams.get_highest_resolution().download(self.main_dir + '/vids', vid_name)
            print()


    def create_compilation(self, comp_name, vid_info, show_thumbs=False):
        #os.system("rm final/*")
        videoclips = []
        d = self.main_dir + "/vids"
        tmpctr = 0
        for path in sorted(os.listdir(d)):
            print("processing " + path)
            full_path = os.path.join(d, path)

            # from filename, extract index: "05-[haiku].mp4" -> 4
            vid_index = int(re.findall(r'\d+', path)[0]) - 1

            start, end = vid_info[vid_index].start, vid_info[vid_index].end

            try:
                vid = VideoFileClip(full_path).fx(afx.audio_normalize)
            except ZeroDivisionError as e:
                print("Error: " + str(e))
                print("Likely due to audio normalization; handling...")
                vid = VideoFileClip(full_path)

            vid = vid.subclip(start, end)
            # so that all clips will fit nicely on a 720p canvas:
            vid = vid.resize(height=720)
            # place on background of 720p resolution.
            # (needed so that text appears on top-left corner of 720p screen
            # and not the corner of the narrower video)
            vid = vid.on_color(size=(1280, 720), col_opacity=1.0)

            hyphen = path.index("-")
            file_ext = path.rfind(".")
            title = path[(hyphen+1) : file_ext].replace("_", " ").replace('\\', '')

            txtClip = TextClip(title, color='white', font="Verdana", fontsize=30)
            txtClip = txtClip.on_color(size=(int(txtClip.w*1.05), int(txtClip.h*1.75)), color=(0,0,0), col_opacity=0.7)

            composed_clip = CompositeVideoClip([vid, txtClip]).set_duration(vid.duration)
            if show_thumbs:
                composed_clip.show()
                time.sleep(0.5)
            videoclips.append(composed_clip)

        if show_thumbs:
            # close pygame window -- it was opened at `composed_clip.show()` just above
            pygame.quit()

        compilation = concatenate_videoclips(videoclips, method="compose")

        print("writing compilation...")
        compilation.write_videofile(self.main_dir + "/final/" + comp_name + ".mp4")
