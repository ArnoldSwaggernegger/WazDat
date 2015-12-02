import soundfiles
import fingerprint

if __name__ == "__main__":

    signal = soundfiles.load_wav("test/muziek.wav")
    fingerprint.get_fingerprints(signal)

    # create classifier from database

    # get arguments

    # get input file fingerprints

    # match fingerprints using the classifier

    # print output
