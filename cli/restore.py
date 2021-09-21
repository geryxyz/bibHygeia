import argparse
import logging

import original
import util

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
logger.addHandler(handler)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="restore.py",
        description='bibHygeia Restore: Restore or drop saved states.',
        epilog='Restore is part of bibHygeia toolkit.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input_folder', type=str, required=True,
                        help='input folder to searching original files recursively')
    parser.add_argument('--drop_original', type=util.bool_switch, required=False, default=False,
                        help='remove all original files')
    parser.add_argument('--log', type=str, default='INFO', required=False,
                        help='level of log messages to display')

    args = parser.parse_args()

    logger.setLevel(logging.getLevelName(args.log))

    if args.drop_original:
        logger.info('dropping saved states')
        originals = original.drop_original_states(args.input_folder)
        logger.info('{} original files were dropped'.format(len(originals)))
    else:
        logger.info('restore saved states')
        originals = original.restore_original_states(args.input_folder)
        logger.info('{} original files were restored'.format(len(originals)))
