import argparse
import time
from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.node import OVSController

parser = argparse.ArgumentParser(description="Run experiment")
parser.add_argument('--manual', help='Manual mininet commands', action='store_true')
args = parser.parse_args()

PORT = 8888
class DaytonaTopo(Topo):
  "Simple topology for bufferbloat experiment."

  def build(self, n=2):
    client = self.addHost('client')
    server = self.addHost('server')
    switch = self.addSwitch('s0')
    self.addLink(client, switch, bw=100, delay="5ms", max_queue_size=20, loss=0)
    self.addLink(server, switch, bw=100, delay="5ms", max_queue_size=20, loss=0)
    return

topo = DaytonaTopo()
net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, controller = OVSController)
net.start()
dumpNodeConnections(net.hosts)
# This performs a basic all pairs ping test.
net.pingAll()

client = net.get('client')
server = net.get('server')

client.cmd("iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP")

if args.manual:

  server.popen("python webserver.py", shell=True)
  time.sleep(1)

  client.popen("./normalTransmission.py %s %s" % (server.IP(), PORT), shell=True).wait()
  #client.popen("./dupACKs.py %s %s" % (server.IP(), PORT), shell=True).wait()
  #client.popen("./splitACKs.py %s %s" % (server.IP(), PORT), shell=True).wait()
  #client.popen("./opACKs.py %s %s" % (server.IP(), PORT), shell=True).wait()

  time.sleep(5.5)

  server.popen("pgrep -f webserver.py | xargs kill -9", shell=True).wait()

else:
  CLI(net)

net.stop()
