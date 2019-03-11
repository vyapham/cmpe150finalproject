CMPE 150 Final Project

Hosts:
	Name: h10
	MAC address: 00:00:00:00:00:00:01
	IP Address: 10.0.1.10/24

	Name: h20
	MAC address: 00:00:00:00:00:00:02
	IP Address: 10.0.2.20/24

	Name: h30
	MAC address: 00:00:00:00:00:00:03
	IP Address: 10.0.3.30/24

	Name: server
	MAC address: 00:00:00:00:00:00:04
	IP Address: 10.0.4.10/24

	Name:trusted
	MAC address: 00:00:00:00:00:00:05
	IP Address: 104.82.214.112/24

	Name:untrusted
	MAC address: 00:00:00:00:00:00:06
	IP Address: 156.134.2.12/24

Switches:
	s1: Floor 1 Switch
	s2: Floor 2 Switch
	s3: Floor 3 Switch
	s4: Core Switch
	s5: Data Center Switch

Logic:
	First, check if packet type is IP or not
	If the packet type is not IP, just flood
	
	If the packet type is IP, then for each switch, check destination IP and source IP to decide which port to send the packet to.

	For switches s1, s2 s3, s5 (all switches except the core switch), check destination ip and send to an appropriate port.

	The Core Switch (s4) is the main part of this logic
	Check dstip:
	   if dstip is trusted: send to port 4
	   elif dstip is untrusted: send to port 5
	   elif dstip is server: 
	   Check srcip:
		 if srcip is untrusted: Drop packet
		 else: send to port 6
	   else: (this means traffics to h10, h20, h30)
	   Check protocol:
	   	 if protocol is ICMP and srcip is untrusted: Drop packet
		 elif dstip is h10: send to port 1
		 elif dstip is h20: send to port 2
		 elif dstip is h30: send to port 3
		 else (this means somehow dstip and/or srcip is not in the network): Drop packet
		 
	     