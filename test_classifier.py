from database import Database
from soundfiles import load_signal, find_files
from fingerprint import get_tokens
import matplotlib.pyplot as plt
from random import shuffle

n = 662

print "Start testing classifier with {} files\n".format(n)

database = Database("pokemon", replace=False)
classifier = database.as_classifier()

filenames = find_files("audio/pokemon/*.wav")
shuffle(filenames)

correct_match = 0
wrong_match = 0
no_match = 0

wrong_matches = ""
correct_matches = ""
no_matches = ""

for filename in filenames[:n]:
    #print "Classifying {}".format(filename)
    signal = load_signal(filename)
    tokens = get_tokens(signal)
    match = classifier.classify(tokens)

    if match is None:
        #print "-> No match found"
        no_matches += filename.split("/")[2][:-4]
        no_match += 1
    elif match.split("/")[2][:3] == filename.split("/")[2][:3]:
        #print "-> Correct match found"
        correct_match += 1
        correct_matches += filename.split("/")[2][:-4]
    else:
        #print "-> Wrong match found"
        wrong_matches += filename.split("/")[2][:-4]
        wrong_match += 1
        
print "\nDone testing {} files".format(n)
print "{} not matched".format(no_match)
print "{} wrong".format(wrong_match)
print "{} correct".format(correct_match)

print "\n{} offset not matched".format(no_matches.count("offset"))
print "{} offset wrong".format(wrong_matches.count("offset"))
print "{} offset correct".format(correct_matches.count("offset"))

print "\n{} noise not matched".format(no_matches.count("noise"))
print "{} noise wrong".format(wrong_matches.count("noise"))
print "{} noise correct".format(correct_matches.count("noise"))

print "\n{} amp not matched".format(no_matches.count("amp"))
print "{} amp wrong".format(wrong_matches.count("amp"))
print "{} amp correct".format(correct_matches.count("amp"))

plt.pie([correct_match, no_match, wrong_match], labels=["Correct match", "No match", "Wrong match"], colors=["yellowgreen", "yellow", "red"], startangle=90, shadow=False)
plt.axis('equal')
plt.show()  


