# Regenerate reflector_packet_transform.png (single plot, no specific colors)

import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))
plt.axis('off')

plt.text(0.25, 0.6,
         "Received Packet\n\n"
         "Ether: src=A_MAC\n"
         "IP: src=A_IP\n"
         "L4: ICMP/TCP/UDP",
         ha='center', va='center',
         bbox=dict(boxstyle="round,pad=0.5"))

plt.text(0.75, 0.6,
         "Constructed Packet (Non-Sent)\n\n"
         "Ether: src=R_MAC\n"
         "IP: src=R_IP or V_IP\n"
         "L4: copied/adjusted fields\n"
         "Checksums deleted",
         ha='center', va='center',
         bbox=dict(boxstyle="round,pad=0.5"))

plt.annotate("", xy=(0.6, 0.6), xytext=(0.4, 0.6),
             arrowprops=dict(arrowstyle="->"))

transform_path = "reflector_packet_transform.png"
plt.savefig(transform_path, dpi=200)
plt.close()

transform_path
