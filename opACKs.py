#! /usr/bin/env python
from scapy.all import *
import sys
import random
import numpy as np
import subprocess as sp
import threading

IP_DST = sys.argv[1]
DST_PORT =  int(sys.argv[2])
IP_SRC = None
SRC_PORT = random.randint(1024,65535)
data = list()
FileName = "opACK.npy"
MTU = 1500
WAIT_TIME = 0.01
stop = False
FIN = 0x01
currACKNo = 0
startACKNo = 0
MAX_SIZE = 100000

#def sendACK():
#  global t, stop, currACKNo, socket2, startACKNo
#  if currACKNo - startACKNo > MAX_SIZE or not stop:
#    currACKNo += MTU
#    ack_pkt = IP(dst=IP_DST) / TCP(window=65535, dport=DST_PORT, sport=SRC_PORT,
#               seq=our_seq_no, ack=currACKNo, flags='A')
#    t.start()
#    socket2.send(Ether() / ack_pkt)
#    print "Sent %d" % currACKNo


#t = threading.Timer(WAIT_TIME, sendACK)
socket = conf.L2socket(iface="client-eth0")
#socket2 = conf.L2socket(iface="client-eth0")

syn = IP(dst=IP_DST) / TCP(window=65535, sport=SRC_PORT, dport=DST_PORT, flags='S')
IP_SRC = syn[IP].src
SRC_PORT = syn[TCP].sport

print "sending SYN....."
syn_ack = sr1(syn)
initialTs = syn_ack.time
initialSeq = syn_ack[TCP].seq
startACKNo = syn_ack[TCP].seq + 1
currACKNo = startACKNo
print "Received SYN_ACK!"
getStr = 'GET / HTTP/1.1\r\n\r\n'
request = IP(dst=IP_DST) / TCP(window=65535, dport=DST_PORT, sport=SRC_PORT,
             seq=(syn_ack[TCP].ack), ack=(syn_ack[TCP].seq + 1), flags='FA') / getStr

maxACK_num = 0

print "Sending Request..."
socket.send(Ether() / request)
#t.start()


def addACKs(pkt):
  global DST_PORT, IP_DST, data, socket, maxACK_num
  if IP not in pkt:
    return
  if TCP not in pkt:
    return
  if pkt[IP].src != IP_DST:
    return
  if pkt[TCP].sport != DST_PORT:
    return

  data.append((pkt.time - initialTs, pkt[TCP].seq - initialSeq))
  
  ip_total_len = pkt.getlayer(IP).len
  ip_header_len = pkt.getlayer(IP).ihl * 32 / 8
  tcp_header_len = pkt.getlayer(TCP).dataofs * 32 / 8
  tcp_seg_len = ip_total_len - ip_header_len - tcp_header_len
  
  add = 0
  cnt = 2
  if pkt.flags & FIN:
    add = 1
    cnt = 1
    stop = True

  nextACK_num = (pkt[TCP].seq + cnt*tcp_seg_len) + add
  if nextACK_num < maxACK_num:
    return
  maxACK_num = nextACK_num

  for x in xrange(2):
    ack_pkt = IP(dst=IP_DST) / TCP(window=65535, dport=DST_PORT, sport=SRC_PORT,
               seq=(pkt[TCP].ack), ack=(pkt[TCP].seq + (x+1)*tcp_seg_len + add), flags='A')
    socket.send(Ether() / ack_pkt)

print("Sniffing......")
sniff(iface="client-eth0", prn=addACKs, filter="tcp and ip", timeout=4)
numbas = np.asarray(zip(*data))
sp.call(["rm", "-f", FileName], shell=True)
np.save(FileName, numbas)
