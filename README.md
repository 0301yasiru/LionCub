![LionCub Screenshot](https://github.com/0301yasiru/LionCub/blob/master/data/lioncub.jpg)

# LionCub Framework

## What is it, actually?
LionCub Framework is a powerful yet user-friendly hacking framework designed specifically for beginners. It enables users to generate TCP backdoors and keyloggers using its Python 3 source code. Moreover, it provides the ability to interact with compromised computers and gain complete control. Additionally, this framework automates the entire WPA2 WiFi cracking procedure, including wireless adapter configuration, AP listing, de-authentication, and more. It also supports ARP spoofing attacks such as MITM, data sniffing, DNS spoofing, packet injection, JS code injection, and MAC address spoofing attacks.

> **Pssst!!!**
> *These backdoors and keyloggers are highly unique, as they operate independently from your public IP address. Thus, you will maintain a persistent connection with the victim, regardless of how many times your router's IP changes.*

## Can you remain anonymous while using it?
Well, it largely depends on how you employ the framework. You can utilize traditional methods to cover your tracks. However, since it employs an online MySQL service, there may be some traces left behind. To address this concern, you can employ fake identities, VPNs, and onion routing.

## How to install LionCub?
The installation process is relatively simple. However, you must have an online MySQL database in order to fully configure this framework. Here are a few ways to acquire an online database:

1. Create a free account on remotemysql.com (recommended).
2. Use your paid database on any hosting service.
3. Utilize your Apache server with port forwarding (not recommended, as some features may not work).

Once you have your database credentials, you can proceed with the installation of LionCub using the following steps:

1. Launch your Kali Linux machine and navigate to the desired installation folder (e.g., `/opt/`).
   - `cd /opt/`

2. Clone the Git repository into your chosen folder and navigate into it.
   - `git clone https://github.com/0301yasiru/LionCub.git`
   - `cd LionCub`

3. Install the framework using the installation script.
   - `python3 install.py`

4. Start the LionCub framework.
   - `python3 lioncub.py`

If you need to reconfigure or modify the MySQL database settings within the framework, you can use the following command:
- `python3 install.py --configure-mysql`

