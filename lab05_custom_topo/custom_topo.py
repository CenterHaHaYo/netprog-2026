from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel


class CustomTopo(Topo):
    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # TODO 4: link h1, h2, and h3 to s1
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)

        # TODO 5: link h4 to s2
        self.addLink(h4, s2)

        # TODO 6: link s1 to s2 (backbone)
        self.addLink(s1, s2)


def main():
    setLogLevel('info')
    net = Mininet(topo=CustomTopo())
    net.start()
    net.pingAll()
    CLI(net)
    net.stop()


if __name__ == "__main__":
    main()
