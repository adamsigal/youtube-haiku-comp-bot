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
