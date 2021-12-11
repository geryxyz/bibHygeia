import argparse
from src.Command import registered_Commands


def main():
    """
    Main function of the application.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-ni", "--no-interaction", help="No interaction mode", action="store_true")

    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND", required=True)

    for cmd in registered_Commands:
        subparser = subparsers.add_parser(cmd.name, help=cmd.description)
        subparser.set_defaults(func=cmd.run)
        cmd.make_parser(subparser)

    args = parser.parse_args()
    args.func(args)
