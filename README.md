# WireGUI

WireGUI is a lightweight graphical interface for managing WireGuard tunnels on Linux.  
It provides a simple desktop application to enable and disable WireGuard interfaces without using the command line.

The application uses PolicyKit (`pkexec`) to securely perform privileged operations when required.

---

## Features

- Simple GUI for managing WireGuard tunnels
- Enable and disable tunnels with a single click
- Reads and writes configuration files in `/etc/wireguard`
- Secure privilege escalation using PolicyKit (`pkexec`)
- Distributed as a Debian (`.deb`) package

---

## Supported platforms

- Ubuntu
- Linux Mint
- Debian-based Linux distributions

> Designed for desktop Linux systems.  
> X11 is recommended; Wayland support may vary depending on the desktop environment.

---

## Installation

Download the latest `.deb` file from the **GitHub Releases** page and install it using:

```bash
sudo apt install ./wiregui_1.0.0_all.deb
