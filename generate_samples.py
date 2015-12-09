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
		for i in range(len(new_samples)):
			new_samples[i] += (0.5 - random.random())*0.1
			
		suffix += "-noise"

	if random.random() < 0.5:
		'''
		add amplification
		'''
		amp = 1-(random.random()*0.5)
		for i in range(len(new_samples)):
			new_samples[i] *= amp

		suffix += "-amp"

	if random.random() < 0.5:
		'''
		add offset
		'''
		offset = random.random()*20000
		new_samples = np.append(np.zeros(offset),(new_samples))

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




