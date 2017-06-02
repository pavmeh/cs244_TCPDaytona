#! /usr/bin/env python
from scapy.all import *
import sys
import numpy as np
import subprocess as sp
import threading

IP_DST = sys.argv[1]
DST_PORT =  int(sys.argv[2])
IP_SRC = None
IP_SRC_PORT = None
data = list()
startSeqNo = 0
timer = 10
FileName = "opACK.npy"
MTU = 1500
WAIT_TIME = 0.01
stop = False
FIN = 0x01
currACKNo = 0

def addACKs(pkt):
  global DST_PORT, IP_DST, startSeqNo, data, FIN, stop
  data.append((pkt.time, pkt[TCP].seq - startSeqNo))
  if pkt[TCP].flags & FIN:
    stop = True

def pktFilter(pkt):
  global IP_SRC, IP_DST, SRC_PORT, DST_PORT
  return pkt[IP].src == IP_DST and pkt[IP].dst == IP_SRC and pkt[TCP].dport == SRC_PORT and pkt[TCP].sport == DST_PORT

def sendACK():
  global t, stop
  currACKNo += MTU
  pkt = IP(dst=IP_DST) / TCP(dport=IP_DST_PORT, flags='A', ack=currACKNo)
  if not stop:
    t.start()


t = threading.Timer(WAIT_TIME, sendACK)
syn = IP(dst=IP_DST) / TCP(dport=IP_DST_PORT, flags='S')
IP_SRC = syn[IP].src
SRC_PORT = syn[TCP].sport
startSeqNo = syn[TCP].seq
currACKNo = startSeqNo
syn_ack = sr1(syn)
getStr = 'GET / HTTP/1.1\r\n\r\n'
request = IP(dst=IP_DST) / TCP(dport=IP_DST_PORT, sport=syn_ack[TCP].dport,
             seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, flags='A') / getStr
sniff(prn=addACKs, lfiter=pktFilter)
reply = sr(request)
t.start()
np.asarray(zip(*data))
sp.call(["rm", "-f", FileName], shell=True)
