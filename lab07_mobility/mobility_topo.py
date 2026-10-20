import time
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mininet.log import setLogLevel, info

def topology():
    net = Mininet_wifi()

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', position='15,50,0')
    sta2 = net.addStation('sta2', position='85,50,0')
    ap1 = net.addAccessPoint('ap1', ssid='netprog-ap1', mode='g', channel='1',
                             position='20,50,0', range=35, failMode='standalone')
    ap2 = net.addAccessPoint('ap2', ssid='netprog-ap2', mode='g', channel='6',
                             position='80,50,0', range=35, failMode='standalone')

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    net.addLink(ap1, ap2)

    info("*** Starting network\n")
    net.build()
    net.start()
    ap1.cmd('ovs-vsctl set-fail-mode ap1 standalone')
    ap2.cmd('ovs-vsctl set-fail-mode ap2 standalone')
    time.sleep(3)
    sta1.cmd('iw dev sta1-wlan0 connect netprog-ap1')
    sta2.cmd('iw dev sta2-wlan0 connect netprog-ap2')
    time.sleep(2)

    net.pingAll()
    CLI(net)
    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    topology()
