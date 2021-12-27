import argparse
import sys

from openapi.generate.generate import generate


def generate_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--spec", help="Specification file")
    args = parser.parse_args()
    if not args.spec:
        print("Please provide specification file with '-s' option")
        sys.exit(1)
    generate(args.spec)


def run_openapi():
    generate_cli()


if __name__ == "__main__":
    run_openapi()
