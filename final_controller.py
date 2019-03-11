# Final Skeleton
#
# Hints/Reminders from Lab 4:
# 
# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, replacing <PORT> with the port number the 
# switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)
#    msg.idle_timeout = 30
#    msg.hard_timeout = 30
#
#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt

log = core.getLogger()

class Final (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    # This is where you'll put your code. The following modifications have 
    # been made from Lab 4:
    #   - port_on_switch represents the port that the packet was received on.
    #   - switch_id represents the id of the switch that received the packet
    #      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)
    
    msg = of.ofp_flow_mod()
    msg.data = packet_in
    
    non_ip_msg = of.ofp_flow_mod()
    """
    msg.match.dl_type = packet.type
    msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
    self.connection.send(msg)
    """
    
    if packet.type != pkt.ethernet.IP_TYPE:
      non_ip_msg.match.dl_type = packet.type
      non_ip_msg.data = packet_in
      non_ip_msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
      self.connection.send(non_ip_msg)
    else:
      msg.match = of.ofp_match.from_packet(packet)
      ip_packet = packet.payload
      srcip = ip_packet.srcip
      dstip = ip_packet.dstip
      """
      msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
      self.connection.send(msg)
      return
      """

      if switch_id == 1: # s1
        if dstip == '10.0.1.10':
          msg.actions.append(of.ofp_action_output(port = 8))
          self.connection.send(msg)
          #return
        else:
          msg.actions.append(of.ofp_action_output(port = 9))
          self.connection.send(msg)
          #return
      elif switch_id == 2: # s2
        if dstip == '10.0.2.20':
          msg.actions.append(of.ofp_action_output(port = 8))
          self.connection.send(msg)
          #return
        else:
          msg.actions.append(of.ofp_action_output(port = 9))
          self.connection.send(msg)
          #return
      elif switch_id == 3: # s3
        if dstip == '10.0.3.30':
          msg.actions.append(of.ofp_action_output(port = 8))
          self.connection.send(msg)
          #return
        else:
          msg.actions.append(of.ofp_action_output(port = 9))
          self.connection.send(msg)
          #return
      elif switch_id == 5: # Data center switch
        if dstip == '10.0.4.10':
          msg.actions.append(of.ofp_action_output(port = 8))
          self.connection.send(msg)
          #return
        else:
          msg.actions.append(of.ofp_action_output(port = 9))
          self.connection.send(msg)
          #return
      else: # switch_id = 4
        if dstip == '104.82.214.112': # traffic to trusted host
          msg.actions.append(of.ofp_action_output(port = 4))
          self.connection.send(msg)
          #return
        elif dstip == '156.134.2.12': # traffic to untrusted host
          msg.actions.append(of.ofp_action_output(port = 5))
          self.connection.send(msg) 
          #return
        elif dstip == '10.0.4.10': # traffic to server
          if srcip == '156.134.2.12': # untrusted host sending ip packet to server
            msg.actions.append(of.ofp_action_output(port = of.OFPP_NONE))
            self.connection.send(msg)
            #return
          else:
            msg.actions.append(of.ofp_action_output(port = 6))
            self.connection.send(msg)
            #return
        else: # traffic to h10, h20, h30
          if ip_packet.protocol == pkt.ipv4.ICMP_PROTOCOL and srcip == '156.134.2.12': # untrusted host sending icmp packet to h10, h20, h30
            msg.actions.append(of.ofp_action_output(port = of.OFPP_NONE))
            self.connection.send(msg)
            #return
          elif dstip == '10.0.1.10': # traffic to h10
            msg.actions.append(of.ofp_action_output(port = 1))
            self.connection.send(msg) 
            #return
          elif dstip == '10.0.2.20': # traffic to h20
            msg.actions.append(of.ofp_action_output(port = 2))
            self.connection.send(msg)
            #return
          elif dstip == '10.0.3.30':  # traffic to h30
            msg.actions.append(of.ofp_action_output(port = 3))
            self.connection.send(msg)
            #return
          else:
            msg.actions.append(of.ofp_action_output(port = of.OFPP_NONE))
            self.connection.send(msg)
            #return
    return
    

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
