from sys import argv, exit
from os import remove, path
from glob import glob
from database import Database
from soundfiles import find_files, load_signal
from fingerprint import get_tokens

# TODO
# make this program generic:
# requires: database-filename, file expression 
# the second might be hard as terminals automatically expand *
def remove_old(name):
    if path.isfile("/databases" + name):
        remove("/databases" + name)

def find_wav_files(directory):
    return glob(directory + "*.wav")

class Create_Database:
    """
    define name, training set directory and database object of the new database 
    """
    def __init__(self, name, directory):
        self.name = name
        self.directory = directory
        self.database = Database(name)
    
    """
    create a new database from 
    """
    def new_database(self):
        remove_old(self.name)

        audio_files = find_wav_files(self.directory)

        for filename in audio_files:
            with open(filename, "r") as f:
                print "Reading {}".format(filename)
                signal = load_signal(filename)
                print "Analyzing {}".format(filename)
                self.database.add(get_tokens(signal))
                print "Done"

        print "Writing database to disk"
        self.database.save()

        
if __name__ == "__main__":

    if len(argv) < 3:
        print "usage: create_bird_database [database name] [training directory]"
        exit()

    name = argv[1]
    directory = argv[2]

    new_db = Create_Database(name, directory)

    new_db.new_database()

    
            
      
