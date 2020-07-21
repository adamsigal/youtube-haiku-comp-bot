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


import datetime
import praw

# XXX: `title` is the YT vid's title, not the reddit post's title
class VidInfo:
    def __init__(self, submission, title, channel, duration, start, end):
        """
        args:
            submission: (praw.Submission),
        	title:      (string),
        	channel:    (string),
        	duration:   (datetime.timedelta),
        	start:      (int) (seconds),
        	end:        (int) (seconds)
        """
        self.submission = submission
        self.title = title
        self.channel = channel
        self.duration = duration
        self.start = start
        self.end = end

    def print_info(self):
        print("title: " + self.title)
        print("channel: " + self.channel)
        print("duration: " + str(self.duration))
        print("start: " + str(self.start) + "s")
        if self.end is None:
            print("end: " + str(self.end))
        else:
            print("end: " + str(self.end) + "s")
        #print("submission: " + self.submission)
        print()
