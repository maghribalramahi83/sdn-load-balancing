"""
By Maghrib Alramahi - Iraq

Proposed of topology
"""


from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink


def run():
    net = Mininet(controller=RemoteController,
                  switch=OVSSwitch,
                  link=TCLink,
                  autoSetMacs=True)

    # Remote SDN Controller / Load Balancing at 10.0.1.1:6633
    info('*** Adding remote controller\n')
    c0 = net.addController(
        'c0',
        controller=RemoteController,
        ip='10.0.1.1',
        port=6633
    )

    info('*** Adding switch OVS1\n')
    s1 = net.addSwitch('s1', protocols='OpenFlow10')

    info('*** Adding client hosts\n')
    h1 = net.addHost('h1', ip='10.0.0.4/24', defaultRoute=None)
    h2 = net.addHost('h2', ip='10.0.0.5/24', defaultRoute=None)
    h3 = net.addHost('h3', ip='10.0.0.6/24', defaultRoute=None)

    info('*** Adding web servers\n')
    srv1 = net.addHost('srv1', ip='10.0.0.1/24', defaultRoute=None)
    srv2 = net.addHost('srv2', ip='10.0.0.2/24', defaultRoute=None)
    srv3 = net.addHost('srv3', ip='10.0.0.3/24', defaultRoute=None)

    info('*** Creating links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)
    net.addLink(srv1, s1)
    net.addLink(srv2, s1)
    net.addLink(srv3, s1)

    info('*** Starting network\n')
    net.build()
    c0.start()
    s1.start([c0])

    info('*** Network is ready\n')
    info('Clients: h1=10.0.0.4, h2=10.0.0.5, h3=10.0.0.6\n')
    info('Servers: srv1=10.0.0.1, srv2=10.0.0.2, srv3=10.0.0.3\n')
    info('Controller: 10.0.1.1:6633 (OpenFlow 1.0)\n')

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()

-------------------
For Run
sudo python ml_qtlb_topology.py
------------------