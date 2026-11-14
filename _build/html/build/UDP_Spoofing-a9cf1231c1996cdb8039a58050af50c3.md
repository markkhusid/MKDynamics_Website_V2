# CSE543 Information Assurance and Security - UDP Spoofing

Created with Grok Build

```{important}
The submission sent a datagram. This page does not.

The send is replaced by a logger. The function builds an IP/UDP object and prints a one-line summary. It does not open a socket, and it does not transmit. The lab host, the port, and the payload that drew a reply stay off the page.
```

UDP has no handshake. The source address is a field the sender writes. A service that treats that field as identity will trust any host that can compose a datagram. The writeup of the protocol is on the Grokipedia page for the [User Datagram Protocol](https://grokipedia.com/page/User_Datagram_Protocol).

## What the submission was doing

The notebook resolved a lab name, then built one UDP datagram with Scapy. The IP source was not the machine that sent the packet. The payload named a different address, the one where a listener was waiting. The lab service accepted the header source as the caller and delivered its answer to the address in the payload.

That split is the whole trick. The header says who the caller claims to be. The payload says where the answer should go. The service trusted both.

## What this page keeps

The published function keeps the shape of that datagram: an IP header, a UDP header, and a short payload. The addresses are documentation addresses from the TEST-NET range. They are not the lab.

```python
DISABLE_PACKET_INJECTION = True

def safe_send(packet):
    """Stand-in for scapy.sr1. Nothing is transmitted."""
    print("[SAFE MODE] Not sent:", packet.summary())

def build_udp(source_ip, dest_ip, payload):
    # The source address is an argument. UDP does not check
    # that the sender owns it. Scapy fills the checksum from
    # the headers when the object is built.
    return (
        IP(src=source_ip, dst=dest_ip)
        / UDP(sport=40000, dport=40000)
        / payload
    )

packet = build_udp("192.0.2.10", "192.0.2.20", b"demo")
if DISABLE_PACKET_INJECTION:
    safe_send(packet)
```

`192.0.2.0/24` is reserved for documentation. `safe_send` prints a summary such as `IP / UDP 192.0.2.10:40000 > 192.0.2.20:40000`. The original notebook called `sr1` on a real interface. That call is the part that made the lab succeed, and it is not here.

## Why a normal socket cannot do this

A normal UDP socket lets the kernel write the source address. The address it writes is an address of the machine. Setting a different source means building the IP header yourself, which is what Scapy does in the object above. Building the object is not the same as sending it. The published page stops at the object.

## What would have stopped it

- Do not authorize a client from the source address of a UDP datagram.
- Do not treat an address inside the payload as a place to send a secret. If the service must answer someone, answer a session it created, or answer a challenge that only the claimed owner can meet.
- Bind a lab service to the lab network. A packet that claims a source outside that network is not a client.

The original notebook, the listener command, and the value the service returned are not published.
