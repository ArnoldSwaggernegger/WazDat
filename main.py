import soundfiles
import fingerprint
import sys

if __name__ == "__main__":

    tutorial = "use: main.py [database] [signal]"

    try:
        database = database.load(arg[1])
    except:
        print "something went wrong with loading the database\n", tutorial
        sys.exit()

    try:
        signal = soundfiles.load_signal("audio/" + arg[2])
        if signal == None:
            raise
    except:
         print "something went wrong with loading the signal\n", tutorial
         sys.exit()

    # fingerprint.get_fingerprints(signal)

    # create classifier from database

    # get input file fingerprints

    # match fingerprints using the classifier

    # print output
