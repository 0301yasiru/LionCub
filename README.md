# LionCub Framework
## What is it actually?
LionCub Framework is a powerful but simple hacking framework, designed for beginners. It allows you to generate TCP back-doors and key-loggers with its python3 source code. Not only that but also you can interact with hacked computer and gain full control. At the same time, this framework can automate whole WPA2 WiFi cracking procedure (configure wireless adapter, list down APs, de-authentication ...) and you can run ARP spoofing attacks like MITM, sniffing data, DNS spoofing, packet injection, JS code injection and MAC address spoofing attacks.
> **Pssst!!!**
> *These back doors and key-loggers are very unique. Because these back-doors are completely independent from your public IP address! So you will have a persistent connection to the victim no matter how many times your routers IP has changed*

## Can you remain anonymous while using it?
Well, it really depends on the way you use it. You can use same old methods to cover your tracks. But since it uses an online MySQL service it may leave some traces! You can use face identities, VPN and onion routing to solve these problems.

## How to install LionCub?
Installation process is fairly simple. But you must have a online MySQL database in order to completely configure this framework!! Here are some few ways to get online database,

 - Create a free account on remotemysql.com (recommended)
 - Use your payed database on any hosting service
 - Use your apache server with port forwarding (not recommended: some features will not work)

If you have your database credentials you can proceed to installation of LionCub.

 1. Fire up your Kali Linux machine and go to any folder you want to install. (I use opt folder..)
 <br>`cd /opt/`
 2. Clone the git repository to your folder and navigate into it
  <br>`git clone https://github.com/0301yasiru/LionCub.git`
  `cd LionCub`
 3. Install the framework using the installation script
  <br>`python3 install.py`
 4. Start the LionCub framework
  <br>`python3 lioncub.py`

If you want to reconfigure or configure MySQL database setting in the framework you can use the command below.
<br>`python3 install.py --configure-mysql`

