'''
database.py

This file contains a simple JSON storage class.
'''

import json
import os
import sys
import classifier
import soundfiles
import fingerprint


class Database:
    '''A simple JSON storage system.'''

    DBPREFIX = 'databases/'

    def __init__(self, name, replace=False, read=True):
        '''
        Database initializer. Reads database if exists.

        Args:
            name: name of database.
            replace: whether to replace or append database.
            read: whether to load the databse from disk on init.
        '''
        self.replace = replace
        self.read = read
        self.name = self.DBPREFIX + name

        if read:
            self.database = self._read_db()
        else:
            self.database = []

    def add(self, tokens):
        '''
        Pushes a singleton or list of tokens to the database.

        Args:
            tokens: Token or list of Token.
        '''
        if not isinstance(tokens, list):
            tokens = [tokens]

        for token in tokens:
            self._push_token(token)

    def save(self):
        '''Wrapper for internal write.'''
        self._write_db()

    def load(self):
        '''Wrapper for internal read.'''
        self.database = self._read_db()

    def as_classifier(self):
        '''
        Build a Classifier from database.

        Returns:
            Classifier populated with Tokens from database.
        '''
        cl = classifier.Classifier()
        for entry in self.database:
            cl.add_token(
                classifier.Token(
                    entry['fingerprint'],
                    entry['time'],
                    entry['filename']
                )
            )

        return cl

    def populate(self, directory):
        '''
        Analyzes all audio files in a directory and add their fingerprint
        to the database. Writes result to disk when done.

        Args:
            directory: directory containing audio files.
        '''
        audio_files = sorted(soundfiles.find_files(directory + '/*'))

        print "Reading {} files...".format(len(audio_files))

        i = 0
        for filename in audio_files:
            i += 1
            sys.stdout.write(
                '\r - file ' + str(i) + ' of ' + str(len(audio_files))
            )
            signal = soundfiles.load_signal(filename)
            self.add(fingerprint.get_tokens(signal))

        print "\nWriting database to disk..."
        self.save()
        print "Done!"

    def get_size(self):
        '''Returns current size of database'''
        return len(self.database)

    def _exists(self):
        '''Returns whether the current database exists.'''
        return os.path.isfile(self.name)

    def _remove(self):
        '''Removes the database file if exists.'''
        if self._exists():
            os.remove(self.name)

    def _push_token(self, token):
        '''
        Pushes a token to the database.

        Args:
            token: Token.
        '''
        self.database.append(token.as_dict())

    def _read_db(self):
        '''
        Read the stored database JSON.

        Returns:
            JSON content of file.
        '''
        if not self._exists():
            return []

        with open(self.name, "r") as file:
            try:
                return json.load(file)
            except ValueError:
                return []

    def _write_db(self):
        '''Write database to disk.'''

        if not os.path.exists(self.DBPREFIX):
            os.makedirs(self.DBPREFIX)

        if self._exists() and self.replace:
            self._remove()

        with open(self.name, 'w+') as file:
            json.dump(self.database, file)

    def __str__(self):
        '''Returns database name.'''
        return self.name
