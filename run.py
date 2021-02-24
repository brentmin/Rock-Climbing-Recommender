# Brian Cheng
# Eric Liu
# Brent Min

# run.py is a file that 
# [TODO]

import argparse
import time

from src.data.run_data import run_data
from src.model.top_pop import top_pop
from src.functions import get_params

def main(params=None):
    """
    The main function that runs all code. Typically, this function will be called from the command
    line so arguments will be read from there. Optionally, this function can be called from another
    file with input parameters to ignore command line arguments.

    :param:     params      Optional command line arguments in dictionary form. If not None, then
                            command line arguments will be ignored
    """
    # params will only be not None if this function is called from the website
    # in that case, change the behavior of the script accordingly
    if(params != None):
        if(params["recommender"] == "top_pop"):
            return top_pop(None, None, params)
        elif(params["recommender"] == "debug"):
            results = top_pop(None, None, params)
            results["notes"] += f"\nInput is: {str(params)}" \
                f"\nOutput is: {str(results['recommendations'])}"
            return results
        else:
            return str(params)

    # all command line arguments
    # for a description of the arguments, refer to the README.md or run "python run.py -h"
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", action="store_true", help="The program will run data " \
        "scraping code if this flag is present.")
    parser.add_argument("-c", "--clean", action="store_true", help="The program will run data " \
        "cleaning code if this flag is present.")
    parser.add_argument("--data-config", default=["config/data_params.json"], type=str, nargs=1,
        help="Where to find data parameters. By default \"config/data_params.json\".")
    parser.add_argument("-p", "--top_pop", action="store_true", help="The program will run data " \
        "return the top 10 most popular/well received as a csv if this flag is present.")
    parser.add_argument("--test", action="store_true", help="The program will run all code in a " \
        "simplified manner. If this flag is present, it will override all other flags and run " \
        "as if the command \"python run.py -d -c -p\" was run on a small dataset.")
    parser.add_argument("--delete", action="store_true", help="The program will wipe out all data from MongoDB")
    parser.add_argument("--upload", action="store_true", help="The program will upload cleaned data to MongoDB")

    # parse all arguments
    args = vars(parser.parse_args())
    print(args)

    # override args if the test flag is present
    if(args["test"]):
        args["data"] = True
        args["clean"] = True
        args["data_config"] = ["config/data_params.json"]
        args["top_pop"] = True
        args["delete"] = False
        args["upload"] = False
    
    # read the config files
    data_params = get_params(args["data_config"][0])

    # run data code
    run_data(data_params, args)

    # run top pop code if requested
    if(args["top_pop"]):
        print(top_pop(args, data_params, {"num_recs": 10}))

# run.py cannot be imported as a module
if __name__ == '__main__':
    # keep track of how long the program has run for
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
