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
import threading
import time

class Database:
    '''A simple JSON storage system.'''

    DBPREFIX = 'databases/'

    def __init__(self, name, replace=False, read=True):
        '''
        Database initializer. Reads database if exists.

        Args:
            name: name of database.
            replace: whether to replace or append database.
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
        self._read_db()

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

    def populate(self, directory, num_threads=1):
        '''
        Analyzes all audio files in a directory and add their fingerprint
        to the database. Writes result to disk when done.

        Args:
            directory: directory containing audio files.
        '''

        print "Expanding audio file glob..."
        audio_files = sorted(soundfiles.find_files(directory + '/*'))

        print "Found {} files. Loading...".format(len(audio_files))
        # signals = []
        # i = 0
        # for filename in audio_files:
        #     i += 1
        #     sys.stdout.write(
        #         '\r - file ' + str(i) + ' of ' + str(len(audio_files))
        #     )
        #     signals.append(soundfiles.load_signal(filename))

        lock = threading.Lock()

        print "Building {} threads...".format(num_threads)
        threads = []
        part_size = len(audio_files) / num_threads
        for n in range(num_threads):
            part1 = n * part_size
            if n == (num_threads - 1):
                part2 = len(audio_files) - 1
            else:
                part2 = (n + 1) * part_size

            thread = threading.Thread(
                target=self._analyze_files,
                args=[audio_files[part1:part2], lock]
            )
            thread.daemon = True
            threads.append(thread)

        print "Starting {} threads...".format(num_threads)
        for thread in threads:
            thread.start()

        print "Working..."
        for thread in threads:
            thread.join()

        print "Writing database to disk..."
        self.save()
        print "Done!"

    def _analyze_files(self, audio_files, lock):
        '''
        '''
        local_buffer = []
        load_sum = 0.0
        local_buffer_sum = 0.0
        wait_lock = 0.0
        global_buffer = 0.0
        for filename in audio_files:
            x = time.time()
            signal = soundfiles.load_signal(filename)
            load_sum += time.time() - x
            x = time.time()
            local_buffer.extend(fingerprint.get_tokens(signal))
            local_buffer_sum += time.time() - x

        x = time.time()
        with lock:
            wait_lock = time.time() - x
            x = time.time()
            self.add(local_buffer)
            global_buffer = time.time() - x

        print "Timing results:"
        print "Loading files from disk (+resampling): \t\t%f" % load_sum
        print "Getting tokens and adding to local array:\t%f" % local_buffer_sum
        print "Waiting for lock to write to global array: \t%f" % wait_lock
        print "Writing local results to global array: \t\t%f\n\n" % global_buffer

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
