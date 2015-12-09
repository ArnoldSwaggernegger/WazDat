import soundfiles
import fingerprint
import numpy as np
import matplotlib.pyplot as plt

signal = soundfiles.load_wav("training/pokemon/003.wav")

x = []
for i in signal:
    x.append(i)

plt.subplot(411)
plt.title("original")
plt.ylim(-1,1)
plt.plot(x)

'''
fingers =  get_fingerprints(signal, 2048, 8)
time = []
peaks = []

for t, ps in fingers:
    time  += [t] * len(ps)
    peaks += ps

plt.subplot(221)
plt.title("original")
plt.scatter(time, peaks, color="red")
'''

signal = soundfiles.load_wav("audio/pokemon/003-divided.wav")

x = []
for i in signal:
    x.append(i)

plt.subplot(412)
plt.title("divided")
plt.ylim(-1,1)
plt.plot(x)

'''
fingers =  get_fingerprints(signal, 2048, 8)
time = []
peaks = []

for t, ps in fingers:
    time  += [t] * len(ps)
    peaks += ps

plt.subplot(222)
plt.title("amplified")
plt.scatter(time, peaks, color="red")
'''

signal = soundfiles.load_wav("audio/pokemon/003-translated.wav")

x = []
for i in signal:
    x.append(i)

plt.subplot(413)
plt.title("offset")
plt.xlim(20480,40480)
plt.ylim(-1,1)
plt.plot(x)

'''
fingers =  get_fingerprints(signal, 2048, 8)
time = []
peaks = []

for t, ps in fingers:
    time  += [t] * len(ps)
    peaks += ps

plt.subplot(223)
plt.title("offset")
plt.scatter(time, peaks, color="red")
'''

signal = soundfiles.load_wav("audio/pokemon/003-noise.wav")

x = []
for i in signal:
    x.append(i)

plt.subplot(414)
plt.title("noise")
plt.ylim(-1,1)
plt.plot(x)
plt.show()

'''
fingers =  get_fingerprints(signal, 2048, 8)
time = []
peaks = []

for t, ps in fingers:
    time  += [t] * len(ps)
    peaks += ps


plt.subplot(224)
plt.title("noise")
plt.scatter(time, peaks, color="red")
plt.show()
'''