from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel


class MinimalTopo(Topo):
    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        s1 = self.addSwitch('s1')
        self.addLink(h1, s1)
        self.addLink(h2, s1)


def main():
    setLogLevel('info')
    net = Mininet(topo=MinimalTopo())
    net.start()
    net.pingAll()
    CLI(net)
    net.stop()


if __name__ == "__main__":
    main()
