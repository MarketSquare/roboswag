import argparse

from roboswag.generate.generate import generate


def generate_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--spec", help="Specification file")
    args = parser.parse_args()
    generate(args.spec)
