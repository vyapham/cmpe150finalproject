#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
  def build(self):
    
    # Examples!
    # Create a host with a default route of the ethernet interface. You'll need to set the
    # default gateway like this for every host you make on this assignment to make sure all 
    # packets are sent out that port. Make sure to change the h# in the defaultRoute area
    # and the MAC address when you add more hosts!
    h10 = self.addHost('h10', mac='00:00:00:00:00:01', ip='10.0.1.10/24', defaultRoute='h10-eth0')
    h20 = self.addHost('h20', mac='00:00:00:00:00:02', ip='10.0.2.20/24', defaultRoute='h20-eth0')
    h30 = self.addHost('h30', mac='00:00:00:00:00:03', ip='10.0.3.30/24', defaultRoute='h30-eth0')
    
    server = self.addHost('server', mac='00:00:00:00:00:04', ip='10.0.4.10/24', defaultRoute='server-eth0')

    trusted = self.addHost('trusted', mac='00:00:00:00:00:05', ip='104.82.214.112/24', defaultRoute='trusted-eth0')
    untrusted = self.addHost('untrusted', mac='00:00:00:00:00:06', ip='156.134.2.12/24', defaultRoute='untrusted-eth0')

    # Create a switch. No changes here from Lab 1.
    s1 = self.addSwitch('s1')
    s2 = self.addSwitch('s2')
    s3 = self.addSwitch('s3')

    coreSwitch = self.addSwitch('s4')
    
    dataCenterSwitch = self.addSwitch('s5')

    # Connect Port 8 on the Switch to Port 0 on Host 1 and Port 9 on the Switch to Port 0 on 
    # Host 2. This is representing the physical port on the switch or host that you are 
    # connecting to.
    self.addLink(h10, s1, port1=0, port2=8)
    self.addLink(h20, s2, port1=0, port2=8)
    self.addLink(h30, s3, port1=0, port2=8)
    
    self.addLink(dataCenterSwitch, server, port1=8, port2=0)
    self.addLink(coreSwitch, dataCenterSwitch, port1=6, port2=9)

    self.addLink(s1, coreSwitch, port1=9, port2=1)
    self.addLink(s2, coreSwitch, port1=9, port2=2)
    self.addLink(s3, coreSwitch, port1=9, port2=3)
    
    self.addLink(coreSwitch, trusted, port1=4, port2=0)
    self.addLink(coreSwitch, untrusted, port1=5, port2=0)    

def configure():
  topo = final_topo()
  net = Mininet(topo=topo, controller=RemoteController)
  net.start()

  CLI(net)
  
  net.stop()


if __name__ == '__main__':
  configure()
