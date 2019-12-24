import sys
sys.dont_write_bytecode = True

import collector
import parser

def main(argv):
    print """

    Welcome to Taskmaster.

    """

    if len(argv) == 1: ## No file was given, prompt for it.
        env_name = raw_input("Please enter the absolute path of your Avida destination directory: ")

    else:
        env_name = argv[1]

    collect = collector.Collector(env_name)

    ## All our tasks_quality files are in a single directory.
    print "Tasks_quality files copied to " + collect.out_path + " now parsing..."

    parse = parser.Parser(collect.out_path)

    return

main(sys.argv)