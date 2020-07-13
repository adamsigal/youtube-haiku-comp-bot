from compiler import Compiler
import tests


def main():
    compiler = Compiler()
    period = "week"
    max_vids = 20


    submission_list, total_duration, description = compiler.get_submission_list(period=period, max_vids=max_vids)
    #print("Top 20 duration: " + str(total_duration))
    comp_name = compiler.comp_name_gen(period, max_vids)

    # submission_list, description = compiler.shuffle_desc_and_vids(submission_list, description)
    #compiler.write_description(comp_name, description)
    #compiler.download_vids(submission_list)

    compiler.create_compilation(comp_name)

if __name__ == "__main__":
    main()
