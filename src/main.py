import argparse
import src.commands


def main():
    """
    Main function of the application.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-ni", "--no-interaction", help="No interaction mode", action="store_true")
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {src.__version__}")

    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND", required=True)

    for cmd in src.commands.registered_commands:
        subparser = subparsers.add_parser(cmd.name, help=cmd.description)
        subparser.set_defaults(func=cmd.run)
        cmd.make_parser(subparser)

    args = parser.parse_args()
    args.func(args)
