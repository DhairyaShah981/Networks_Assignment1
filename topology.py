from mininet.topo import Topo
from mininet.link import TCLink
from mininet.node import OVSController


class MyTopo(Topo, TCLink, OVSController):
    "Simple topology example."

    def _init_(self):
        "Create custom topo."

        # Initialize topology
        Topo._init_(self)

        # Add hosts and switches
        A = self.addHost('A')
        B = self.addHost('B')
        C = self.addHost('C')
        D = self.addHost('D')
        R1 = self.addSwitch('R1')
        R2 = self.addSwitch('R2')

        # Add links
        L1 = self.addLink(A, R1, cls=TCLink, bw=1000, delay='1ms')
        L5 = self.addLink(D, R1, cls=TCLink, bw=1000, delay='1ms')
        L3 = self.addLink(B, R2, cls=TCLink, bw=1000, delay='1ms')
        L4 = self.addLink(C, R2, cls=TCLink, bw=1000, delay='5ms')
        L5 = self.addLink(R1, R2, cls=TCLink, bw=500, delay='10ms')


topos = {'mytopo': (lambda: MyTopo())}
