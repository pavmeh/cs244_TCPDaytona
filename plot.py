import matplotlib.pyplot as plt
import numpy as np

DupFileName = "dupACK.npy"
SplitFileName = "splitACK.npy"
NormalFileName = "normal.npy"

dupACKs = np.load(DupName)
splitACKs = np.load(SplitFileName)
normalACKs = np.load(NormalFileName)

plt.figure(1)
plt.subplot(211)
plt.Title("Duplicate ACKs")
plt.scatter(*zip(dupACKs))
plt.scatter(*zip(normal))
plt.xlabel("time (s)")
plt.ylabel("Seq Number")

plt.subplot(212)
plt.Title("Split ACKs")
plt.scatter(*zip(splitACKs))
plt.scatter(*zip(normal))
plt.xlabel("time (s)")
plt.ylabel("Seq Number")

plt.savefig('data.png')