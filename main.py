'''
main.py
'''

import argparse
from database import Database
from soundfiles import load_signal
from sys import exit
from fingerprint import get_tokens

if __name__ == "__main__":
    import colors
    c = colors.Colors()

    parser = argparse.ArgumentParser(description='Classify audio.')
    parser.add_argument(
        '-d', metavar='database', type=str, required=True,
        help='Database to use.'
    )
    parser.add_argument(
        '--train', metavar='training files', type=str,
        help='Files to analyze and store in database as training.'
    )
    parser.add_argument(
        '-f', metavar='file', type=str,
        help='File to classify.'
    )

    args = parser.parse_args()

    replace = args.train is not None
    c.notice('Reading database {}...'.format(args.d))
    database = Database(args.d, replace=replace, read=False)
    if database is None:
        c.fail('This database could not be loaded')
        parser.print_help()
        exit()

    if args.train:
        database.populate(args.train)

    if args.f:
        if not database.read:
            c.notice('Loading database from disk...')
            database.load()
            c.succes('Loaded {} entries.'.format(database.get_size()))

        c.notice('Converting database to classifier...')
        classifier = database.as_classifier()

        c.notice('Loading \'{}\' from disk...'.format(args.f))
        signal = load_signal(args.f)
        if signal is None:
            c.fatal('This file could not be loaded')
            parser.print_help()
            exit()

        c.notice('Analyzing \'{}\'...'.format(signal.get_filename()))
        tokens = get_tokens(signal)

        c.notice("Classifying...")
        match = classifier.classify(tokens)

        if match:
            c.notice("File \'{}\' matches with database entry {}".format(
                signal.filename, match
            ))
        else:
            c.fatal(
                "File \'{}\' could not be matched".format(signal.filename)
            )
