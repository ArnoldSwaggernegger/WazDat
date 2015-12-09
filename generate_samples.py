import soundfiles
import random
import matplotlib.pyplot as plt
import wave

directory = "training/pokemon/*.wav"

files = soundfiles.find_files(directory)

for f in files:
	signal = soundfiles.load_signal(f)

	new_samples = signal.samples.tostring()
	print signal.samples
	print new_samples
	
	dest = f.replace("training","audio")
	
	wav = wave.open(dest,'w')
	
	wav.setparams((1, 4, signal.samplerate, len(new_samples), 'NONE', 'not defined'))

	wav.writeframes(new_samples)

	break




