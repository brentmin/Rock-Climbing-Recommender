# Brian Cheng
# Eric Liu
# Brent Min

# run.py is a file that 
# [TODO]

import argparse
import time

from src.data.run_data import run_data
from src.functions import get_params

def main(params=None):
    """
    The main function that runs all code. Typically, this function will be called from the command
    line so arguments will be read from there. Optionally, this function can be called from another
    file with input parameters to ignore command line arguments.

    :param:     params      Optional command line arguments in dictionary form. If not None, then
                            command line arguments will be ignored
    """
    # all command line arguments
    # for a description of the arguments, refer to the README.md or run "python run.py -h"
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", action="store_true", help="The program will run data " \
        "scraping code if this flag is present.")
    parser.add_argument("--data-config", default=["config/data_params.json"], type=str, nargs=1,
        help="Where to find data parameters. By default \"config/data_params.json\"")

    # parse all arguments
    args = parser.parse_args()
    print(args)

    # read the config files
    data_params = get_params(args.data_config[0])

    # if the user requested to run data scraping code
    if(args.data):
        run_data(data_params)

# run.py cannot be imported as a module
if __name__ == '__main__':
    # keep track of how long the program has run for
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
