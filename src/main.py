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

import tests
import argparse
import sys
import os
import datetime
import random

# access priv_utils directory
MAIN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MAIN_DIR + "/private")
import priv_utils

random.seed(1337)


def main(period, time_limit, max_vids, min_score, no_download):
    compiler = Compiler(priv_utils.get_yt(), priv_utils.get_reddit(), MAIN_DIR)

    tests.download_test(MAIN_DIR, "are_ya_winnin_son", "https://www.youtube.com/watch?v=xCLTw1L-H5g&feature=emb_title")
    return


    # for debugging
    fetch = False
    write = True
    vid_pkl_path = MAIN_DIR + '/src/vid_info.pkl'


    # vid info will either be fetched or read from file
    if fetch:
        print("fetching") # TODO: remove
        vid_info, total_duration = compiler.fetch_vid_info(period=period, time_limit=time_limit, max_vids=max_vids, min_score=min_score)

        # only write if new values have been fetched
        if write:
            print("writing") # TODO: remove
            utils.write_pkl(vid_pkl_path, (vid_info, total_duration))
    else:
        print("reading") # TODO: remove
        #vid_info, total_duration = utils.read_vid_info(vid_pkl_path)
        vid_info, total_duration = utils.read_pkl(vid_pkl_path)


    print("total duration: " + str(total_duration) + "\n")
    for i in range(len(vid_info)):
        vid_info[i].print_info()

    comp_name = compiler.comp_name_gen(period, max_vids)

    # shuffle vid order so that worst vids aren't always last
    random.shuffle(vid_info)
    description = compiler.gen_description(vid_info)
    compiler.write_description(comp_name, description)
    compiler.download_vids(vid_info)

    compiler.create_compilation(comp_name, vid_info)

if __name__ == "__main__":
    # These variables are instanciated to make it easier to see default vals
    default_period = "week"
    default_max_vids = 5 #TODO: make positional
    default_min_score = 0
    default_no_download = False # by default we download the videos
    default_time_limit = datetime.timedelta.max

    parser = argparse.ArgumentParser(prog='YouTube Haiku Compilation Bot')
    parser.add_argument("-p", "--period",       help="options: 'week', 'month', 'year', 'all time'",
                            default=default_period,      metavar='')

    parser.add_argument("-mv", "--max-vids",    help="max number of vids for a given compilation",
                            default=default_max_vids,    metavar='', type=int)

    parser.add_argument("-ms", "--min-score",   help="min number of upvotes to get into the compilation",
                            default=default_min_score,   metavar='', type=int)

    parser.add_argument("-nd", "--no-download", help="indicates to not download videos locally",
                            default=default_no_download, action="store_true")

    parser.add_argument("-tl", "--time-limit",  help="max duration of compilation in minutes",
                            default=None,                metavar='', type=int)

    parser.add_argument("-y", "--yes",  help="assume 'yes' to all prompts",
                            default=False,               action="store_true")

    args = parser.parse_args()
    assert args.period in ('week', 'month', 'year', 'all time')
    assert (args.max_vids >= 0) and (args.min_score >= 0)

    # time limit must be converted to timedelta
    if args.time_limit:
        time_limit = datetime.timedelta(minutes = args.time_limit)
    else:
        time_limit = default_time_limit

    # make sure the command is what they actually intended
    doublecheck = "'Top " + str(args.max_vids) + " of the " + args.period
    if args.no_download:
        doublecheck = doublecheck + ", no download"
    if args.time_limit:
        doublecheck = doublecheck + ", time limit: " + str(args.time_limit) + " mins"
    if args.min_score:
        doublecheck = doublecheck + ", minimum score: " + str(args.min_score)
    doublecheck = doublecheck + "'"

    print(doublecheck)

    while True:
        if args.yes:
            print("Is this command correct? [Y/n] y")
            break

        choice = input("Is this command correct? [Y/n] ").lower()
        if choice in ('y', 'yes'):
            break
        elif choice in ('n', 'no'):
            print("Try again, use '--help' if needed.")
            exit(0)
        else:
            sys.stdout.write("Please respond with 'y' or 'n' (or 'yes' or 'no').\n")

    main(args.period, time_limit, args.max_vids, args.min_score, args.no_download)
