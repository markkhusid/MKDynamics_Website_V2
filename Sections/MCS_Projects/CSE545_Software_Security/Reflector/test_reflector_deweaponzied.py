import importlib
import sys
from contextlib import redirect_stdout
from io import StringIO

import pytest
import scapy.all as scapy


# --------------------------------------------------------------------------------------
# Utility: import reflector safely (because argparse runs at import time)
# --------------------------------------------------------------------------------------

def import_reflector_with_argv(
    *,
    interface="lo",
    victim_ip="192.0.2.10",
    victim_mac="aa:bb:cc:dd:ee:10",
    reflector_ip="192.0.2.20",
    reflector_mac="aa:bb:cc:dd:ee:20",
):
    argv_saved = sys.argv[:]
    try:
        sys.argv = [
            "reflector.py",
            "--interface", interface,
            "--victim-ip", victim_ip,
            "--victim-ethernet", victim_mac,
            "--reflector-ip", reflector_ip,
            "--reflector-ethernet", reflector_mac,
        ]

        if "reflector" in sys.modules:
            mod = importlib.reload(sys.modules["reflector"])
        else:
            mod = importlib.import_module("reflector")

        return mod
    finally:
        sys.argv = argv_saved


def capture_stdout(fn, *args, **kwargs):
    buf = StringIO()
    with redirect_stdout(buf):
        fn(*args, **kwargs)
    return buf.getvalue()


def print_test_header(name, packet):
    print("\n" + "=" * 70)
    print(f"TEST: {name}")
    print("-" * 70)
    print("Packet summary:")
    print("  ", packet.summary())
    print("=" * 70)


def print_test_result(success):
    if success:
        print("\n>>> RESULT: PASS")
    else:
        print("\n>>> RESULT: FAIL")
    print("=" * 70 + "\n")


@pytest.fixture
def reflector_module():
    mod = import_reflector_with_argv()
    mod.DISABLE_LIVE_SNIFFING = True
    mod.DISABLE_PACKET_INJECTION = True
    return mod


# --------------------------------------------------------------------------------------
# Verbose Tests
# --------------------------------------------------------------------------------------

def test_arp_request_to_victim_verbose(reflector_module):
    test_name = "ARP request to victim triggers ARP constructor (safe mode)"

    attacker_ip = "192.0.2.99"
    attacker_mac = "de:ad:be:ef:00:01"

    pkt = (
        scapy.Ether(src=attacker_mac, dst="ff:ff:ff:ff:ff:ff")
        / scapy.ARP(op=1, psrc=attacker_ip,
                    pdst=reflector_module.victim_ip,
                    hwsrc=attacker_mac)
    )

    print_test_header(test_name, pkt)

    output = capture_stdout(reflector_module.handle_packet, pkt)

    print("Function exercised: handle_packet -> spoof_ARP_from_Reflector_to_Attacker")
    print("\nCaptured output:")
    print(output)

    success = (
        "[ARP]" in output
        and "Constructed (non-sent) forged ARP reply" in output
        and "[SAFE MODE] Blocked packet injection" in output
    )

    print_test_result(success)
    assert success


def test_icmp_to_victim_verbose(reflector_module):
    test_name = "ICMP to victim triggers reflector ICMP constructor (safe mode)"

    attacker_ip = "192.0.2.99"
    attacker_mac = "de:ad:be:ef:00:02"

    pkt = (
        scapy.Ether(src=attacker_mac, dst=reflector_module.reflector_ethernet)
        / scapy.IP(src=attacker_ip, dst=reflector_module.victim_ip)
        / scapy.ICMP(type=8, code=0, id=0x1234, seq=1)
        / b"payload"
    )

    print_test_header(test_name, pkt)

    output = capture_stdout(reflector_module.handle_packet, pkt)

    print("Function exercised: handle_packet -> send_ICMP_packet_from_Reflector_to_Attacker")
    print("\nCaptured output:")
    print(output)

    success = (
        "[DISPATCH] ICMP to victim" in output
        and "Constructed (non-sent) reflected ICMP packet" in output
        and "[SAFE MODE] Blocked packet injection" in output
    )

    print_test_result(success)
    assert success


def test_udp_to_victim_verbose(reflector_module):
    test_name = "UDP to victim triggers UDP constructor (safe mode)"

    attacker_ip = "192.0.2.99"
    attacker_mac = "de:ad:be:ef:00:03"

    pkt = (
        scapy.Ether(src=attacker_mac, dst=reflector_module.reflector_ethernet)
        / scapy.IP(src=attacker_ip, dst=reflector_module.victim_ip)
        / scapy.UDP(sport=5555, dport=4444)
        / scapy.Raw(load=b"hello")
    )

    print_test_header(test_name, pkt)

    output = capture_stdout(reflector_module.handle_packet, pkt)

    print("Function exercised: handle_packet -> send_UDP_packet")
    print("\nCaptured output:")
    print(output)

    success = (
        "[DISPATCH] UDP" in output
        and "Constructed (non-sent) reflected UDP packet" in output
        and "[SAFE MODE] Blocked packet injection" in output
    )

    print_test_result(success)
    assert success


def test_tcp_to_reflector_verbose(reflector_module):
    test_name = "TCP to reflector triggers TCP constructor (safe mode)"

    attacker_ip = "192.0.2.99"
    attacker_mac = "de:ad:be:ef:00:04"

    pkt = (
        scapy.Ether(src=attacker_mac, dst=reflector_module.reflector_ethernet)
        / scapy.IP(src=attacker_ip, dst=reflector_module.reflector_ip)
        / scapy.TCP(sport=12345, dport=80, seq=100, ack=0, flags="S")
    )

    print_test_header(test_name, pkt)

    output = capture_stdout(reflector_module.handle_packet, pkt)

    print("Function exercised: handle_packet -> send_TCP_packet")
    print("\nCaptured output:")
    print(output)

    success = (
        "[DISPATCH] TCP" in output
        and "Constructed (non-sent) reflected TCP packet" in output
        and "[SAFE MODE] Blocked packet injection" in output
    )

    print_test_result(success)
    assert success


def test_safety_flags_verbose(reflector_module):
    test_name = "Safety flags remain enabled"

    print("\n" + "=" * 70)
    print(f"TEST: {test_name}")
    print("=" * 70)

    print("DISABLE_LIVE_SNIFFING =", reflector_module.DISABLE_LIVE_SNIFFING)
    print("DISABLE_PACKET_INJECTION =", reflector_module.DISABLE_PACKET_INJECTION)

    success = (
        reflector_module.DISABLE_LIVE_SNIFFING is True
        and reflector_module.DISABLE_PACKET_INJECTION is True
    )

    print_test_result(success)
    assert success