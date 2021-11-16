import argparse
from src.Command import registered_Commands


def main(is_ci=False):
    """
    Main function of the application.
    """

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='command', required=True)

    for cmd in registered_Commands:
        subparser = subparsers.add_parser(cmd.name, help=cmd.description)
        subparser.set_defaults(func=cmd.run)
        cmd.make_parser(subparser)

    args = parser.parse_args()
    args.func(args)
