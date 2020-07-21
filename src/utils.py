import re
from urllib.parse import urlparse, parse_qs
import pickle


# shouts to Willem Van Onsem:
# https://stackoverflow.com/questions/45579306/get-youtube-video-url-or-youtube-video-id-from-a-string-using-regex
def get_yt_id(url):
    u_pars = urlparse(url)
    quer_v = parse_qs(u_pars.query).get('v')
    if quer_v:
        return quer_v[0]
    pth = u_pars.path.split('/')
    if pth:
        return pth[-1]

def get_start_end(url):
    """
    Args:
        url (str): YouTube url
    Returns:
        start (int): start time in seconds
        end (int): end time in seconds (None if not specified)
    """
    #url = "https://www.youtube.com/embed/c_jomXhjUjI?t=1h3m40s"
    if "end=" in url:
        # 'end=' followed by # of seconds
        end = re.findall(r'end=\d+', url)[0]
        #print(end)
        end = int(end.split("=")[-1])
    else:
    	end = None
    #print("end is " + str(end))

    if "start=" in url:
        # 'start=' followed by # of seconds
        st = re.findall(r'start=\d+', url)[0]
        #print(st)
        st = int(st.split("=")[-1])
    # number following '?t=' either in seconds or #h#m#s
    elif ("?t=" in url) or ("&t=" in url):
        # '?t=' or '&t=' followed by numbers, 'h', 'm', or 's'
        st = re.findall(r'[\?|\&]t=[hms0-9]+', url)[0]
        #print("regex 1: " + st)
        st = st.split("=")[-1]
        #print("split at '=': " + st)
        if re.search(r'[hms]', st):
            hours, minutes, seconds = '0', '0', '0'
            if "h" in st:
                hours, st = st.split('h')
            if "m" in st:
                minutes, st = st.split('m')
            if "s" in st:
                seconds, st = st.split('s')
            st = int(hours)*3600 + int(minutes)*60 + int(seconds)
        else:
            st = int(st)
    else:
    	st = 0

    #print("start is " + str(st))
    return (st, end)



# Shouts to Greenstick:
# https://stackoverflow.com/a/34325723/7077792
# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

# write vid info to file; used to reduce api query usage
def write_vid_info(path, vid_info, total_duration):
    with open(path, 'wb') as f:
        pickle.dump((vid_info, total_duration), f, pickle.HIGHEST_PROTOCOL)

# read vid info from file; used to reduce api query usage
def read_vid_info(path):
    try:
        with open(path, 'rb') as f:
            vid_info, total_duration = pickle.load(f)
            return vid_info, total_duration
    except Exception as e:
        print("Error retrieving vid info: ", e)
