# CSE543 Information Assurance and Security - TCP Spoofing

Created with Grok Build

TCP names a connection by addresses, ports, and sequence numbers. The sequence number is supposed to be hard to guess. This lab asked for a conversation that appeared to come from a host that was not the one sending the packets.

## What the submission did

The submission watched the sequence numbers a lab server chose, then sent packets whose source address was not the machine that transmitted them. A raw socket let the script fill in that address itself, instead of leaving it to the operating system. The server accepted a guessed sequence and continued the exchange.

## Why that is a weak authenticator

A source address is a field the sender writes. It is not proof of who sent the packet. The sequence number is the only secret in a classic handshake, and only when it is unpredictable. When the numbers follow a pattern, a third party can try likely values until one is accepted. The host that owns the address is not in the conversation.

Current stacks randomize the initial sequence number and drop packets that do not belong to a socket they opened. An application should still not treat a finished handshake as proof of a user. That proof belongs in a protocol above TCP.

## What stayed off this page

The packet layouts, the search over sequence numbers, the lab host name, and the script that sent the packets are not published.
