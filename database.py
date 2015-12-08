import json
import os
import classifier
import soundfiles
import fingerprint


class Database:
    '''
    '''

    DBPREFIX = 'databases/'

    def __init__(self, name, replace=False):
        '''
        '''
        self.replace = replace
        self.name = self.DBPREFIX + name
        self.database = self._read_db()

    def add(self, tokens):
        '''
        '''
        if not isinstance(tokens, list):
            tokens = [tokens]

        for token in tokens:
            self._push_token(token)

    def save(self):
        '''
        '''
        self._write_db()

    def as_classifier(self):
        '''
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
        '''
        audio_files = sorted(soundfiles.find_files(directory + '/*'))

        print "Reading {} files".format(len(audio_files))

        for filename in audio_files:
            print "{}:\n - loading...".format(filename)
            signal = soundfiles.load_signal(filename)

            print " - analyzing..."
            self.add(fingerprint.get_tokens(signal))

        print "Writing database to disk..."
        self.save()
        print "Done!"

    def _exists(self):
        '''
        '''
        return os.path.isfile(self.name)

    def _remove(self):
        '''
        '''
        os.remove(self.name)

    def _push_token(self, token):
        '''
        '''
        self.database.append(token.as_dict())

    def _read_db(self):
        '''
        '''
        if not self._exists():
            return []

        with open(self.name, "r") as file:
            try:
                return json.load(file)
            except ValueError:
                return []

    def _write_db(self):
        '''
        '''

        if not os.path.exists(self.DBPREFIX):
            os.makedirs(self.DBPREFIX)

        if self._exists() and self.replace:
            self._remove()

        with open(self.name, 'w+') as file:
            json.dump(self.database, file)

    def __str__(self):
        '''
        '''
        return self.name
