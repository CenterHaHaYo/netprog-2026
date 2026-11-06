import json
import time

from mn_wifi.net import Mininet_wifi
from mininet.log import setLogLevel, info

DISTANCES = [5, 10, 15, 20, 25, 30]


def run_iperf3_udp(server_sta, client_sta, server_ip,
                   duration=5, bitrate="10M"):
    server_sta.cmd(
        f"iperf3 -s -1 -J > /tmp/server_{client_sta.name}.json &"
    )
    time.sleep(1)

    # TODO 1
    client_sta.cmd(
        f"iperf3 -c {server_ip} -u -b {bitrate} "
        f"-t {duration} -J "
        f"> /tmp/client_{client_sta.name}.json"
    )
    time.sleep(1)

    with open(f"/tmp/client_{client_sta.name}.json") as f:
        data = json.load(f)

    if "error" in data:
        raise RuntimeError(data["error"])

    # TODO 2
    summary = data["end"]["sum"]

    return {
        "throughput_mbps": summary["bits_per_second"] / 1e6,
        "jitter_ms": summary["jitter_ms"],
        "loss_percent": summary["lost_percent"],
    }


def topology():
    net = Mininet_wifi()

    try:
        sta1 = net.addStation("sta1", position="5,50,0")
        sta2 = net.addStation("sta2", position="0,50,0")
        ap1 = net.addAccessPoint('ap1', ssid='netprog-ap', mode='g', channel='1', position='0,50,0', range=30, failMode= 'standalone',)
        net.configureWifiNodes()

        net.addLink(sta1, ap1)
        net.addLink(sta2, ap1)

        net.build()
        net.start()

        time.sleep(3)

        print("sta1 IP:", sta1.IP())
        print("sta2 IP:", sta2.IP())
        print("sta1 Wi-Fi:", sta1.cmd("iw dev sta1-wlan0 link"))
        print("sta2 Wi-Fi:", sta2.cmd("iw dev sta2-wlan0 link"))
        print(sta1.cmd(f"ping -c 3 -W 2 {sta2.IP()}"))

        results = []

        for d in DISTANCES:
            info(f"*** Measuring at distance {d}m\n")

            # TODO 3
            sta1.setPosition(f"{d},50,0")
            time.sleep(1)

            r = run_iperf3_udp(sta2, sta1, sta2.IP())

            # TODO 4
            r["distance_m"] = d

            results.append(r)
            print(d, r, flush=True)

        with open("results.json", "w") as f:
            json.dump(results, f, indent=2)

    finally:
        net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    topology()
