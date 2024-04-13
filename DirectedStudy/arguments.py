from sys import argv
from argparse import ArgumentParser

def get_cli_arguments():
    parser = ArgumentParser("Offline transaction processor")
    parser.add_argument("--username", required=True)
    parser.add_argument("--phone_number", type=int, required=True)
    parser.add_argument("--initial_balance", type=int, required=True)
    parser.add_argument("--currency", required=True)

    args = parser.parse_args()

    return args

    params = dict()
    for arg in argv[1:]:
        if arg.startswith("--"):
            if "=" in arg:
                eq_index = arg.index("=")
                key = arg[2:eq_index]
                value = arg[eq_index+1:]
                params[key] = value
    return params