from compiler import Compiler
import tests
import private
import argparse

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
    max_vids = 20


    submission_list, total_duration, description, start_ends = compiler.get_submission_list(period=period, max_vids=max_vids)
    #print("Top 20 duration: " + str(total_duration))
    comp_name = compiler.comp_name_gen(period, max_vids)

    submission_list, description, start_ends = compiler.shuffle_vids(submission_list, description, start_ends)
    compiler.write_description(comp_name, description)
    compiler.download_vids(submission_list)

    compiler.create_compilation(comp_name, start_ends)

if __name__ == "__main__":
    main()
