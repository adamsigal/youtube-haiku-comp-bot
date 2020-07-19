# By Adam Sigal
import utils

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

class Compiler:
    def __init__(youtube, reddit):
        self.youtube = youtube
        self.reddit = reddit

    # Fetches the submissions from reddit
    def get_submission_list(self, period="month", time_limit=datetime.timedelta.max, max_vids=50, min_score=0):
        """
        Args:
            period (str): "week", "month", "year", "all time"
            time_limit (timedelta): time limit for a given compilation
            max_vids (int): max number of vids for a given compilation
            min_score (int): min # of upvotes to get into the compilation
        Returns:
            submission_list (praw.models.Submission[]): posts gathered from reddit
            total_duration (timedelta): sum of videos' lengths
            description (string[]): list of strings each containing info on posts
            start_ends ( (int, int)[] ): list of (start, end) tuples
        """

        submission_list = []
        ctr = 0
        total_duration = datetime.timedelta(seconds = 0)
        description = []
        start_ends = []
        for submission in self.reddit.subreddit("youtubehaiku").top(period):
            if (ctr >= max_vids):
                #print("ctr value: " + str(ctr))
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
                start, end = get_start_end(submission.url)
                start = int(start)
                start_td = datetime.timedelta(seconds = start)

                if end is not None:
                    end = int(end)
                    duration_timedelta = datetime.timedelta(seconds = end) - start_td
                else:
                    duration_str = response['items'][0]['contentDetails']['duration']
                    duration_timedelta = isodate.parse_duration(duration_str) - start_td


                if (total_duration+duration_timedelta > time_limit) or (submission.score < min_score):
                    break

                title = response['items'][0]['snippet']['title']
                channel = response['items'][0]['snippet']['channelTitle']
                # TODO: will total_duration appear as a clickable timestamp in the yt description?
                description.append(str(total_duration) + ' "' + title + '" - ' + channel + "\n" + submission.url)

                submission_list.append(submission)
                total_duration += duration_timedelta
                ctr += 1
                start_ends.append( (start, end) )


            except Exception as e:
                print("Error with post: ", e)
                print("Post title: '%s'. \nPost url: %s\nContinuing..." % (submission.title, submission.url))

        print("length of list: " + str(len(submission_list)))
        print("total duration: " + str(total_duration))
        return (submission_list, total_duration, description, start_ends)

    # Might be obselete with total_duration included in get_submission_list()
    def get_total_duration(self, submissions):
        total_duration = datetime.timedelta(seconds = 0)

        for submission in submissions:
            vid_id = get_yt_id(submission.url)
            request = self.youtube.videos().list(
                part="ContentDetails",
                id=vid_id
            )
            response = request.execute()

            duration_str = response['items'][0]['contentDetails']['duration']
            duration_timedelta = isodate.parse_duration(duration_str)

            total_duration += duration_timedelta

        return total_duration


    def shuffle_vids(self, submission_list, description, start_ends):
        # zip together these 2 lists so that their elements can be shuffled in the same order
        zip_subs_desc = list(zip(submission_list, description, start_ends))
        # randomize order so that the worst ones aren't last
        random.shuffle(zip_subs_desc)

        # unzip to (submission_list, description, start_ends)
        return zip(*zip_subs_desc)


    # TODO: for highest quality (1080p and above) you need to merge
    # separate audio and video streams
    # https://python-pytube.readthedocs.io/en/latest/user/quickstart.html
    def download_vids(self, submissions, delete_past_vids=True):
        if delete_past_vids:
            os.system("rm ../vids/*.mp4")

        # for having consistent naming of downloaded video files
        l = len(submissions)
        decimal_places = math.ceil(math.log10(l))
        format_string = "{:0" + str(decimal_places) + "d}"
                    # TODO: remove 10, i'm just using it to skip to where prob is
        for i in range(len(submissions)):
    #         try:
            #pre_prefix = "Downloading: " + submissions[i].title + "\n"

            utils.printProgressBar(i+1, l, prefix = 'Downloading videos:', suffix = 'Complete', length = 50)
            # TODO: remove, this is for testing

            vid = YouTube(submissions[i].url)
            streams = vid.streams.filter(progressive=True)

            vid_name = format_string.format(i+1) + "-" + submissions[i].title.replace(" ", "_")
    #         print(vid_name)
    #         continue
            streams.get_highest_resolution().download('../vids', vid_name)
                #vid_paths.append("./vids/" + vid_name + ".mp4")
    #         except:
    #             print("Error with post: '%s'. \nurl: %s\nContinuing..." % (submissions[i].title, submissions[i].url))

    # Generates name of the compilation based on date and number of videos
    def comp_name_gen(self, period, num_vids):
        if period in ('day', 'week', 'month', 'year'):
            return str(datetime.datetime.date(datetime.datetime.now())) + "_top_" + str(num_vids) + "_of_" + period
        else:
            raise Exception("invalid period argument, must be one of: 'day', 'week', 'month', 'year'")

    # Description still expected in list form
    def write_description(self, comp_name, description):
        str_description = "\n\n".join(description)

        # hashtags from video titles will automatically be added to the
        # compilation's hastags, so I just remove them
        str_description = str_description.replace('#', '')

        f = open("../final/" + comp_name + "_description" , "w")
        f.write(str_description)
        f.close()
        print("Description written to file: " + "../final/" + comp_name + "_description")



    # TODO: make sure that subclips are working correctly
    # https://zulko.github.io/moviepy/getting_started/quick_presentation.html
    def create_compilation(self, comp_name, start_ends):
        #os.system("rm final/*")

        videoclips = []
        d = "../vids"
        for path in sorted(os.listdir(d)):
            full_path = os.path.join(d, path)
            # from filename, extract index: "05-[haiku].mp4" -> 4
            vid_index = int(re.findall(r'\d+', t)[0]) - 1
            start, end = start_ends[vid_index]

            vid = VideoFileClip(full_path).fx(afx.audio_normalize)
            # TODO: check that it's fine if end=None
            vid = vid.subclip(start, end)
            # so that all clips will fit nicely on a 720p canvas:
            vid = vid.resize(height=720)
            # place on background of 720p resolution.
            # (needed so that text appears on top-left corner of 720p screen
            # and not the corner of the narrower video)
            vid = vid.on_color(size=(1280, 720), col_opacity=1.0)

            hyphen = path.index("-")
            mp4 = path.index(".mp4")
            title = path[(hyphen+1) : mp4].replace("_", " ")

            #print("'" + title + "' size (before resize): (" + str(vid.h) + ", " + str(vid.w) + ")")
            ## had the resizing line from above here.
            #print("'" + title + "' size (after resize): (" + str(vid.h) + ", " + str(vid.w) + ")")
            # TODO: I don't think most of this actually works rn
            txtClip = TextClip(title, color='white', font="Verdana",
                               fontsize=30)
            txtClip = txtClip.on_color(size=(int(txtClip.w*1.05), int(txtClip.h*1.75)), color=(0,0,0), col_opacity=0.7)

            composed_clip = CompositeVideoClip([vid, txtClip]).set_duration(vid.duration)

            composed_clip.show()
            time.sleep(0.5)
            videoclips.append(composed_clip)
            #print(full_path)

        # close pygame window -- it was opened at `composed_clip.show()` just above
        pygame.quit()
        #print(videoclips)
        # TODO: shuffle this earlier so that i can make the description correspond

        #return # TODO: remove
        compilation = concatenate_videoclips(videoclips, method="compose")
        # normalize audio
        ##compilation = compilation.fx(afx.audio_normalize)

        # TODO: give good name
        compilation.write_videofile("../final/" + comp_name + ".mp4")
