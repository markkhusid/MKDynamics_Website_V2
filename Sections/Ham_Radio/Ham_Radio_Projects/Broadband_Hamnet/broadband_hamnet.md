# Broadband Hamnet

Created with Grok Build

Two Linksys WRT54GL routers, reflashed with Broadband-Hamnet firmware 3.1.0, carry a mesh between two laptops. The photographs and the clip are from 17 November 2018. [Broadband-Hamnet](https://www.broadband-hamnet.org/), formerly HSMM-Mesh, is the firmware project. The firmware note on the original page points at the [software download](https://www.broadband-hamnet.org/software-download.html).

Each node is opened in a browser at `http://localnode:8080`.

## Node 1

The status page is AC2LH-Node1. The Wi-Fi address is 10.68.158.69/8 and the LAN address is 10.36.242.41/29. The laptop on that LAN is 10.36.242.43. The WAN address and the default gateway are both none. The firmware line reads 3.1.0 and the configuration is mesh. Signal, noise, and ratio read −16 / −92 / 76 dB.

The router clock says Saturday 1 January 2000, 01:09:35 UTC, and the uptime is 1:09. The laptop clock in the photograph reads 6:07 AM on 17 November 2018.

```{figure} images/node1_status.jpg
:width: 800
:align: center
:class: clickable-figure

Broadband-Hamnet status for AC2LH-Node1, opened at localnode:8080
```

## The WRT54GL

Node 1's radio is a Linksys WRT54GL Wireless-G router. In this photograph the power lamp, the WLAN lamp, and LAN port 1 are lit.

```{figure} images/wrt54gl.jpg
:width: 800
:align: center
:class: clickable-figure

Linksys WRT54GL used as Broadband-Hamnet node 1
```

## Node 2

The second laptop is logged into AC2LH-Node2. The Wi-Fi address is 10.68.157.58/8 and the LAN address is 10.36.233.209/29. This laptop is 10.36.233.212. Signal, noise, and ratio read −21 / −90 / 69 dB. The firmware is again 3.1.0 in mesh configuration, and the uptime is 12:30. The router clock still reads 1 January 2000. Wireshark is open on the same screen, with the display filter `tcp and not icmp`.

```{figure} images/node2_status.jpg
:width: 800
:align: center
:class: clickable-figure

AC2LH-Node2 status, with Wireshark on the mesh LAN
```

## The link

The clip is 56 seconds at 640 by 480. It was recorded on the laptop attached to node 2.

The mesh-status page lists AC2LH-Node2 as the local host and AC2LH-Node1 as the current neighbor. The link quality to that neighbor is 84%, and the neighbor advertises a service named `mkdwww`. A few minutes after the still above, the same status page reads −23 / −92 / 69 dB, with an uptime of 12:53.

The rest of the clip is a page fetched across that link. Wireshark shows an HTTP GET between 10.36.233.212, the laptop on node 2, and 10.36.242.43, the laptop on node 1. Node 1 forwards port 80 to the laptop on its LAN, and that laptop answers with Apache. The browser on node 2 requests the name `ac2lh-node1`.

:::{figure} broadband_hamnet_link.mp4
:align: center

Mesh status on node 2, then an HTTP fetch of the site served by the laptop on node 1
:::
