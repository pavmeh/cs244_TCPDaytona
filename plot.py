import matplotlib; matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

DupFileName = "dupACK.npy"
SplitFileName = "splitACK.npy"
NormalFileName = "normal.npy"
OpFileName = "opACK.npy"

#dupACKs = np.load(DupFileName)
splitACKs = np.load(SplitFileName)
normalACKs = np.load(NormalFileName)
#opACKs = np.load(OpFileName)

plt.figure(1)
#plt.subplot(211)
#plt.title("Duplicate ACKs")
#plt.scatter(*zip(dupACKs))
#plt.scatter(*zip(normalACKs))
#plt.xlabel("time (s)")
#plt.ylabel("Seq Number")

plt.subplot(212)
plt.title("Split ACKs")
plt.scatter(*zip(splitACKs))
plt.scatter(*zip(normalACKs))
plt.xlabel("time (s)")
plt.ylabel("Seq Number")

#plt.subplot(213)
#plt.title("OP ACKs")
#plt.scatter(*zip(opACKs))
#plt.scatter(*zip(normalACKs))
#plt.xlabel("time (s)")
#plt.ylabel("Seq Number")

plt.savefig('data.png')
