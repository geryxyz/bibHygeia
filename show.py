import argparse
import logging
import os

from upgrade import Upgrade

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
logger.addHandler(handler)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="show.py",
        description='bibHygeia Show: Displays details.',
        epilog='Show is part of bibHygeia toolkit.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='input file or folder to inspect')
    parser.add_argument('--id', type=str, required=False, default=None,
                        help='Regular expression to select BibTeX id for the entry to inspect')
    parser.add_argument('--log', type=str, default='INFO', required=False,
                        help='level of log messages to display')

    args = parser.parse_args()

    logger.setLevel(logging.getLevelName(args.log))

    input_ext = os.path.splitext(args.input)[-1].lower()
    if input_ext == '.ugr':
        upgrade: Upgrade = Upgrade.load(args.input)
        for i, replacement in enumerate(upgrade):
            if not args.id or (replacement.new == args.id or replacement.original == args.id):
                logger.info('entry#{}'.format(i))
                logger.info('{} --> {}'.format(replacement.original, replacement.new))
                try:
                    logger.info('reason: {}'.format(replacement.reason.human_readable()))
                except AttributeError:
                    logger.warning('reason of type {} does not support inspection'.format(type(replacement.reason).__name__))
    else:
        logger.error("The '{}' are not supported".format(input_ext))
