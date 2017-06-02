#! /usr/bin/env python
from scapy.all import *
import sys
import numpy as np
import subprocess as sp

IP_DST = sys.argv[1]
DST_PORT =  int(sys.argv[2])
IP_SRC = None
SRC_PORT = None
data = list()
startSeqNo = 0
FileName = "normal.npy"

def addACKs(pkt):
  global DST_PORT, IP_DST, startSeqNo, data
  if IP not in pkt:
    return
  if TCP not in pkt:
    return
  if pkt[IP].src != IP_DST:
    return
  if pkt[TCP].sport != DST_PORT:
    return
  data.append((pkt.time, pkt[TCP].seq - startSeqNo))

syn = IP(dst=IP_DST) / TCP(dport=DST_PORT, flags='S')
IP_SRC = syn[IP].src
SRC_PORT = syn[TCP].sport
startSeqNo = syn[TCP].seq
syn_ack = sr1(syn)
getStr = 'GET / HTTP/1.1\r\n\r\n'
request = IP(dst=IP_DST) / TCP(dport=DST_PORT, sport=syn_ack[TCP].dport,
             seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, flags='A') / getStr
sniff(prn=addACKs, filter="tcp and ip", timeout=5)
reply = sr(request)
numbas = np.asarray(zip(*data))
sp.call(["rm", "-f", FileName], shell=True)
np.save(FileName, numbas)
