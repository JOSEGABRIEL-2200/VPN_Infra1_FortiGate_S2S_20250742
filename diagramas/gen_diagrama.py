import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse, FancyArrowPatch

fig, ax = plt.subplots(figsize=(16, 10.5), dpi=150)
ax.set_xlim(0, 160); ax.set_ylim(0, 105); ax.axis("off")
fig.patch.set_facecolor("white")

INK = "#1f2937"; MUTED = "#6b7280"
C_USR = "#2563eb"; C_FGT = "#dc2626"; C_SW = "#0f766e"; C_ISP = "#7c3aed"; C_WEB = "#d97706"; C_MG = "#9ca3af"

def box(x, y, w, h, title, lines, color, fs=9.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5,rounding_size=1.8",
                                linewidth=2, edgecolor=color, facecolor="white", zorder=3))
    ax.text(x + w/2, y + h - 3.0, title, ha="center", va="center", fontsize=12, fontweight="bold", color=color, zorder=4)
    for i, t in enumerate(lines):
        ax.text(x + w/2, y + h - 6.8 - i*3.1, t, ha="center", va="center", fontsize=fs,
                color=INK, family="DejaVu Sans Mono", zorder=4)

def link(p1, p2, label=None, color=INK, lw=2.2, ls="-", off=(0, 1.8), fs=8.5):
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, lw=lw, ls=ls, zorder=2, solid_capstyle="round")
    if label:
        ax.text((p1[0]+p2[0])/2 + off[0], (p1[1]+p2[1])/2 + off[1], label, ha="center", va="center",
                fontsize=fs, color=MUTED, zorder=5, bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))

ax.text(80, 102, "Infraestructura 1 — VPN IPsec Site-to-Site entre dos FortiGate", ha="center", fontsize=17, fontweight="bold", color=INK)
ax.text(80, 98.3, "Jose Gabriel Feliz Maria · Matrícula 2025-0742 · Seguridad de Redes (ITLA)", ha="center", fontsize=10.5, color=MUTED)

# Cloud
ax.add_patch(Ellipse((80, 87), 50, 12.5, facecolor="#f3f4f6", edgecolor=C_MG, lw=2, zorder=1))
ax.text(80, 88.7, "NAT-INTERNET (Cloud0)", ha="center", fontsize=11.5, fontweight="bold", color="#4b5563")
ax.text(80, 85, "192.168.182.0/24 · Internet vía NAT de VMware", ha="center", fontsize=8.8, color=INK, family="DejaVu Sans Mono")

# Devices
box(64, 52, 32, 21, "ISP (Cisco IOL)", ["e0/0  200.7.42.1/30", "e0/1  200.7.42.5/30", "e0/2  DHCP (Internet)", "NAT/PAT hacia Internet"], C_ISP)
box(12, 48, 34, 27, "Fortinet1", ["Sitio Usuarios", "port1 MGMT 192.168.182.41", "port2 WAN  200.7.42.2/30", "port3 LAN  10.7.42.1/25", "DHCP .10 – .126 · NAT"], C_FGT)
box(114, 48, 34, 27, "Fortinet2", ["Sitio Servidor", "port1 MGMT 192.168.182.42", "port2 WAN  200.7.42.6/30", "port3 LAN  10.7.42.129/28", "NAT"], C_FGT)
box(16, 13, 26, 18, "SW-A (Cisco L2)", ["e0/0 acceso VLAN 10", "e0/1 acceso VLAN 10", "e0/2-3 VLAN 999 off"], C_SW)
box(-2+2, -1+2, 1, 1, "", [], "white")  # spacer (invisible)
box(118, 13, 26, 18, "Kali-WEB (Cloud1)", ["Servidor HTTPS :443", "10.7.42.130/28", "GW 10.7.42.129"], C_WEB)
box(52, 13, 26, 18, "PC-USUARIO (VPCS)", ["VLAN 10 · DHCP", "10.7.42.10/25", "GW 10.7.42.1"], C_USR)

# Physical links
link((46.5, 63), (63.5, 63), "port2 ↔ e0/0")
link((96.5, 63), (113.5, 63), "e0/1 ↔ port2")
link((80, 73.5), (80, 81), "e0/2", off=(4, 0))
link((29, 47.5), (29, 31.5), "port3 ↔ e0/0", off=(0, 0))
link((42.5, 22), (51.5, 22), "e0/1", off=(0, 2))
link((131, 47.5), (131, 31.5), "port3", off=(0, 0))

# Management links (dashed)
link((62, 85), (29, 75.5), "port1 (gestión)", color=C_MG, ls="--", lw=1.6, off=(-3, 2))
link((98, 85), (131, 75.5), "port1 (gestión)", color=C_MG, ls="--", lw=1.6, off=(3, 2))

# VPN tunnel
arc = FancyArrowPatch((46, 50), (114, 50), connectionstyle="arc3,rad=0.30", arrowstyle="<|-|>",
                      mutation_scale=16, lw=2.6, color=C_FGT, ls="--", zorder=2)
ax.add_patch(arc)
ax.text(80, 36.6, "Túnel IPsec Site-to-Site  200.7.42.2 ⇄ 200.7.42.6", ha="center", fontsize=10.5, fontweight="bold", color=C_FGT,
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none"))
ax.text(80, 33.4, "Fase 2: 10.7.42.0/25 ⇄ 10.7.42.128/28", ha="center", fontsize=9.3, color=INK, family="DejaVu Sans Mono",
        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"))

ax.text(80, 4, "El ISP no conoce las redes 10.7.42.x: el Usuario solo llega al Servidor a través del túnel "
        "(con el túnel caído, la ruta blackhole descarta el tráfico).", ha="center", fontsize=9.3, color=MUTED)

plt.savefig("topologia_infra1.png", bbox_inches="tight", facecolor="white")
print("ok")
