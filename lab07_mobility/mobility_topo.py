import time
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mininet.log import setLogLevel, info

SETUP = 5

def topology():
    net = Mininet_wifi()

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', position='15,50,0')
    sta2 = net.addStation('sta2', position='85,50,0')
    sta3 = net.addStation('sta3', position='10,50,0')
    ap1 = net.addAccessPoint('ap1', ssid='netprog-ap1', mode='g', channel='1',
                             position='20,50,0', range=35, failMode='standalone')
    ap2 = net.addAccessPoint('ap2', ssid='netprog-ap2', mode='g', channel='6',
                             position='80,50,0', range=35, failMode='standalone')

    net.configureWifiNodes()
    net.addLink(ap1, ap2)

    info("*** Starting mobility\n")
    net.startMobility(time=0)
    net.mobility(sta3, 'start', time=1 + SETUP, position='10,50,0')
    net.mobility(sta3, 'stop', time=20 + SETUP, position='90,50,0')
    net.stopMobility(time=21 + SETUP)

    net.build()
    net.start()
    ap1.cmd('ovs-vsctl set-fail-mode ap1 standalone')
    ap2.cmd('ovs-vsctl set-fail-mode ap2 standalone')

    time.sleep(3)
    sta1.cmd('iw dev sta1-wlan0 connect netprog-ap1')
    sta2.cmd('iw dev sta2-wlan0 connect netprog-ap2')
    sta3.cmd('iw dev sta3-wlan0 connect netprog-ap1')
    time.sleep(2)
    
    info("*** Monitoring sta3 association during mobility\n")
    for t in range(22):
        x = sta3.position[0]
        assoc = sta3.params.get('associatedTo') or sta3.wintfs[0].associatedTo
        print(f"t={t}s sta3 x={x:.2f}m associated to: {assoc}")
        time.sleep(1)

    CLI(net)
    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    topology()

