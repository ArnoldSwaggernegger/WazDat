import json
import os.path
import classifier


class Database:
    '''
    '''

    DBPREFIX = 'databases/'

    def __init__(self, name):
        '''
        '''
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

    def _push_token(self, token):
        '''
        '''
        self.database.append(token.as_dict())

    def _read_db(self):
        '''
        '''
        mode = 'r'
        if os.path.isfile(self.name):
            mode = 'rw'

        with open(self.name, mode) as file:
            try:
                data = json.load(file)
            except ValueError:
                data = []
            return data

    def _write_db(self):
        '''
        '''
        with open(self.name, 'w') as file:
            json.dump(self.database, file)
