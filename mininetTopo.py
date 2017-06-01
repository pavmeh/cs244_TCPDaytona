from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.util import dumpNodeConnections
from mininet.cli import CLI

PORT = 8888
class DaytonaTopo(Topo):
  "Simple topology for bufferbloat experiment."

  def build(self, n=2):
    h1 = self.addHost('h1')
    h2 = self.addHost('h2')
    switch = self.addSwitch('s0')
    self.addLink(h1, switch, bw=100, delay="5ms", max_queue_size=20, loss=0)
    self.addLink(h2, switch, bw=100, delay="5ms", max_queue_size=20, loss=0)
    return

topo = DaytonaTopo()
net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
net.start()
dumpNodeConnections(net.hosts)
# This performs a basic all pairs ping test.
net.pingAll()

h1 = net.get('h1')
h2 = net.get('h2')
h2.popen("./mTCPserver %s %s" % (h2.IP(), PORT), shell=True)
h1.popen("./normalTransmission.py %s %s" % (h2.IP(), PORT), shell=True).wait()
h1.popen("./dupACKs.py %s %s" % (h2.IP(), PORT), shell=True).wait()
h1.popen("./splitACKs.py %s %s" % (h2.IP(), PORT), shell=True).wait()
Popen("pgrep -f mTCPserver | xargs kill -2", shell=True).wait()



net.stop()