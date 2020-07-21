from compiler import Compiler
import tests
import argparse
import sys
import os

# access private directory
MAIN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MAIN_DIR + "/private")
import priv_utils

def parse():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("--period", "-p", help="options: 'week', 'month', 'year', 'all time'", default="week")
    parser.add_argument("--max_vids", "-v", help="max number of vids for a given compilation", type=int, default=5)
    parser.add_argument("--min_score", "-s", help="min number of upvotes to get into the compilation", type=int, default=None)
    # TODO: add later
    # parser.add_argument("--time_limit", "-tl", help="time limit for a given compilation")

    args = parser.parse_args()

def main():
    compiler = Compiler(private.get_yt(), private.get_reddit())
    period = "week"
    max_vids = 5


    vid_info, total_duration = compiler.fetch_vid_info(period=period, max_vids=max_vids)
    print("total duration: " + str(total_duration) + "\n")
    for i in range(len(vid_info)):
        vid_info[i].print_info()

    # comp_name = compiler.comp_name_gen(period, max_vids)
    #
    # #submission_list, description, start_ends = compiler.shuffle_vids(submission_list, description, start_ends)
    # compiler.write_description(comp_name, description)
    # compiler.download_vids(submission_list)
    #
    # compiler.create_compilation(comp_name, start_ends)

if __name__ == "__main__":
    main()
