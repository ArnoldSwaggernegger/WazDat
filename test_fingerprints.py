import fingerprint
import soundfiles
import matplotlib.pyplot as plt

pokemon_nr = "103" # "003"

filenames = [
    "training/pokemon/{}.wav".format(pokemon_nr),
    "audio/pokemon/{}-multiplied.wav".format(pokemon_nr),
    "audio/pokemon/{}-noise.wav".format(pokemon_nr),
    "audio/pokemon/{}-translated.wav".format(pokemon_nr)
]

n = len(filenames)
    
fig, ax = plt.subplots(n)

for i in xrange(n):
    filename = filenames[i]
    signal = soundfiles.load_signal(filename)
    fingerprints = fingerprint.get_fingerprints(signal)
    
    x = [time for (time, peaks) in fingerprints for freq in peaks]
    y = [freq for (time, peaks) in fingerprints for freq in peaks]
    
    if "translated" in filename:
        # the translated file has a 1sec offset (10 timesteps)
        x = [e - 10 for e in x]
    
    for h in xrange(0, 128, 16):
        ax[i].axhline(y=h, color="grey", alpha=0.25)
    
    plot = ax[i].scatter(x, y, color="red")
    ax[i].set_xlim((0, 10))
    ax[i].set_ylim((0, 128))
    ax[i].legend([plot], [filename], loc="lower right")

plt.show()
