import soundfiles
import random
import matplotlib.pyplot as plt
import wave
import numpy as np
import os

if not os.path.exists("audio/pokemon"):
    os.makedirs("audio/pokemon")

directory = "training/pokemon/*.wav"

files = soundfiles.find_files(directory)

for f in files:
	signal = soundfiles.load_signal(f)

	'''
	initialize the suffix of the new file and the new samples
	'''
	suffix = ""
	new_samples = signal.samples

	if random.random() < 0.5:
		'''
		add noise
		'''
        new_samples += 0.05 - 0.1 * np.random.rand(len(new_samples))
        suffix += "-noise"

	if random.random() < 0.5:
		'''
		add amplification
		'''
		new_samples *= 0.5 + (0.5 * random.random())
		suffix += "-amp"

	if random.random() < 0.5:
		'''
		add offset
		'''
		offset = int(random.random() * 16384)
		new_samples = np.append(np.zeros(offset), (new_samples))

		suffix += "-offset"
	
	'''
	convert to string
	'''
	new_samples = (new_samples * 2**31).astype(np.int32).tostring()

	dest = f.replace("training","audio")
	dest = dest.split(".")[0] + suffix + "." + dest.split(".")[1]
	
	wav = wave.open(dest,'w')
	
	wav.setparams((1, 4, signal.samplerate, len(new_samples), 'NONE', 'not defined'))

	wav.writeframesraw(new_samples)
