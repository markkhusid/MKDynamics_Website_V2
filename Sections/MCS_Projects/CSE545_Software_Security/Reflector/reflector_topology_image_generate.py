# Regenerate reflector_topology.png (single plot, no specific colors)

import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))
plt.axis('off')

attacker = (0.1, 0.6)
reflector = (0.5, 0.8)
victim = (0.9, 0.6)
lan = (0.5, 0.3)

plt.text(*attacker, "Attacker\n(A)", ha='center', va='center',
         bbox=dict(boxstyle="round,pad=0.4"))
plt.text(*reflector, "Reflector Script\n(R)", ha='center', va='center',
         bbox=dict(boxstyle="round,pad=0.4"))
plt.text(*victim, "Victim\n(V)", ha='center', va='center',
         bbox=dict(boxstyle="round,pad=0.4"))
plt.text(*lan, "LAN / Switch", ha='center', va='center',
         bbox=dict(boxstyle="round,pad=0.4"))

plt.annotate("", xy=reflector, xytext=attacker, arrowprops=dict(arrowstyle="->"))
plt.annotate("", xy=victim, xytext=attacker, arrowprops=dict(arrowstyle="->"))
plt.annotate("", xy=attacker, xytext=victim, arrowprops=dict(arrowstyle="->"))

topology_path = "reflector_topology.png"
plt.savefig(topology_path, dpi=200)
plt.close()

topology_path
