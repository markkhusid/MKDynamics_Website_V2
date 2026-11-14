# CSE543 Information Assurance and Security - UDP Spoofing

Created with Grok Build

UDP has no handshake. A datagram carries a source address because the sender wrote one in the header. Nothing in UDP checks that the sender owns that address.

## What the submission did

The submission sent a datagram whose source address was chosen in the script, toward a lab service that replied to whatever source the packet claimed. The service treated that address as the caller. The reply followed the forged address.

## The lesson

A service that authorizes a client from the source address of a UDP datagram will trust any host that can send a packet. The fix is an authenticator inside the payload, or a challenge that only the claimed source can answer.

## What stayed off this page

The script, the lab host, and the value the service returned are not published.
