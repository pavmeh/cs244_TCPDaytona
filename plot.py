import matplotlib; matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

DupFileName = "dupACK.npy"
SplitFileName = "splitACK.npy"
NormalFileName = "normal.npy"
OpFileName = "opACK.npy"

dupACKs = np.load(DupFileName)
splitACKs = np.load(SplitFileName)
normalACKs = np.load(NormalFileName)
opACKs = np.load(OpFileName)

plt.figure(1)
plt.subplot(311)
plt.title("Duplicate ACKs")
plt.scatter(*zip(dupACKs), label="Duplicate ACKs")
plt.scatter(*zip(normalACKs), label="Normal")
plt.xlabel("time (s)")
plt.ylabel("Seq Number")
plt.legend(loc="lower right")

plt.subplot(312)
plt.title("Split ACKs")
plt.scatter(*zip(splitACKs), label="Split ACKs")
plt.scatter(*zip(normalACKs), label="Normal")
plt.xlabel("time (s)")
plt.ylabel("Seq Number")
plt.legend(loc="lower right")

plt.subplot(313)
plt.title("Optimistic ACKs")
plt.scatter(*zip(opACKs), label="Optimistic ACKs")
plt.scatter(*zip(normalACKs), label="Normal")
plt.xlabel("time (s)")
plt.ylabel("Seq Number")
plt.legend(loc="lower right")

plt.savefig('data.png')
