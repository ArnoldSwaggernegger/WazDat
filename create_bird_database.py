from os import remove
from database import Database
from soundfiles import find_files, load_signal
from fingerprint import get_tokens

# TODO
# make this program generic:
# requires: database-filename, file expression 
# the second might be hard as terminals automatically expand *

if __name__ == "__main__":

    remove(Database.DBPREFIX + "vogels") 
    database = Database("vogels")
    
    for filename in ["training/track01_ijsvogel.wav", "training/track03_goudvink.wav"]: #find_files("training/*.wav"):
        with open(filename, "r") as f:
            print "Reading {}".format(filename)
            signal = load_signal(filename)
            print "Analyzing {}".format(filename)
            database.add(get_tokens(signal))
            print "Done"
            
    print "Writing database to disk"
    database.save()  
