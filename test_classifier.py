from database import Database
from soundfiles import load_signal, find_files
from fingerprint import get_tokens
import matplotlib.pyplot as plt
from random import shuffle

n = 600

print "Start testing classifier with {} files\n".format(n)

database = Database("pokemon", replace=False)
classifier = database.as_classifier()

filenames = find_files("training/pokemon/*.wav")
shuffle(filenames)

correct_match = 0
wrong_match = 0
no_match = 0

for filename in filenames[:n]:
    print "Classifying {}".format(filename)
    signal = load_signal(filename)
    tokens = get_tokens(signal)
    match = classifier.classify(tokens)
    
    if match is None:
        print "-> No match found"
        no_match += 1
    elif match == filename:
        print "-> Correct match found"
        correct_match += 1
    else:
        print "-> Wrong match found"
        wrong_match += 1
        
print "\nDone testing {} files".format(n)
print "{} correct".format(correct_match)
print "{} wrong".format(wrong_match)
print "{} not matched".format(no_match)

plt.pie([correct_match, no_match, wrong_match], labels=["Correct match", "No match", "Wrong match"], colors=["yellowgreen", "yellow", "red"], startangle=90, shadow=False)
plt.axis('equal')
plt.show()  


