from database import Database
from soundfiles import find_files, load_signal

# TODO
# make this program generic:
# requires: database-filename, file expression 
# the second might be hard as terminals automatically expand *

if __name__ == "__main__":

    database = Database("vogels")
    
    for filename in find_files("training/*.wav"):
        with open(filename, "r") as f:
            print "Reading {}".format(filename)
            signal = load_signal(filename)
            print "Analyzing {}".format(filename)
            database.add(signal.get_tokens())
            print "Done"
            
    print "Writing database to disk"
    database.save()  
