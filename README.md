<h1>SIPCheck v.3.0</h1>

## Introduction

SIPCheck is a tool that watch the authentication of users of Asterisk and bans automatically if some user (or bot) try to register o make calls using wrong passwords. 

Unlike Fail2Ban, SIPCheck manage, not just the attacker, also the clients that you have trust so if you have SIP users that has demostrated that they are trusted, it will don't ban although we receive wrong password, because it would means that lots of SIP clients behind of this IP could be banned too.

For this reason, we have redesign from scratch this application with several features respect of older versions.

- **Easier**: Easy of installing, configure and execute.
- **Resources**: Oriented to great systems with a lot number of simoultaneous calls, avoiding access to log files and parsing of lots of real time information.
- **Persistent**: Don't worry if you have to restart the application or the system, SIPCheck keep the attackers into the firewall when it start again.
- **Confidable**: New system of expire time will keep the IPTable clean of old attackers avoiding unending and uncontrollable lists.
- **Control**: Using the small config file `sipcheck.conf`, you can control the number of tries before to ban the access, the time that attackers will be on the firewall and the time that suspected users will be under watch.

## Requirements

SIP Check requires been executed in the same system where Asterisk run. (it could run in other system but the firewall will be used in the same system where it run).
SIPCheck needs **root privileges** to be able to insert and remove rules into the firewall.

### Python 3
SIPCheck 3 works using Python 3 and the libraries defined in `requirements.txt`

### Asterisk manager account
`/etc/asterisk/manager.conf` must have some manager user like this (change user and password variables):

You have create a new user of [Asterisk Manager Interface](https://wiki.asterisk.org/wiki/display/AST/The+Asterisk+Manager+TCP+IP+API).
```ini
[CHANGETHISUSER]
secret = CHANGETHISPASSWORD
deny = 0.0.0.0/0.0.0.0
permit = 127.0.0.1/255.255.255.255
read = security
write = system
```

Once created/modified this user, you have to reload manager configuration:
```bash
asterisk -rx 'manager reload'
```

## How to Install

```bash
# Download github repository
git clone https://github.com/sinologicnet/sipcheck.git /opt/sipcheck
cd /opt/sipcheck

# Update repositories
apt-get update

# Install PIP for Python3
apt-get install python3-pip

# Install the libraries required 
pip3 install -r requirements.txt

# Copy the sample of configuration file into a official configuration file
cp sipcheck.conf.sample sipcheck.conf

# Edit this file to configure SIPCheck
nano sipcheck.conf

# Make executable sipcheck.py
chmod 777 sipcheck.py

# Insert the script into systemd
cp /opt/sipcheck/sipcheck.service /etc/systemd/system/
systemctl enable sipcheck

# Start the application
systemctl start sipcheck

# Check if everything is working fine
tail -f /var/log/sipcheck.log
```

## Example of use
```log
2020-03-14 19:25:51,309 INFO: -----------------------------------------------------
2020-03-14 19:25:51,309 INFO: Starting SIPCheck 3 ...
2020-03-14 19:25:51,309 INFO: + Added 185.53.88.49,1584140431 into blacklist again from the time: 1584140431
2020-03-14 19:25:51,309 INFO: BL: Detected attack from IP: '185.53.88.49' (Banning address)
2020-03-14 19:25:51,312 INFO: + Added 195.154.28.205,1584140431 into blacklist again from the time: 1584140431
2020-03-14 19:25:51,312 INFO: BL: Detected attack from IP: '195.154.28.205' (Banning address)
2020-03-14 19:25:51,313 INFO: + Added 92.246.85.154,1584140431 into blacklist again from the time: 1584140431
2020-03-14 19:25:51,313 INFO: BL: Detected attack from IP: '92.246.85.154' (Banning address)
2020-03-14 19:25:51,315 INFO: + Added 113.141.67.163,1584140431 into blacklist again from the time: 1584140431
2020-03-14 19:25:51,315 INFO: BL: Detected attack from IP: '113.141.67.163' (Banning address)
2020-03-14 19:25:51,317 INFO: + Added 192.227.132.19,1584140431 into blacklist again from the time: 1584140431
2020-03-14 19:25:51,317 INFO: BL: Detected attack from IP: '192.227.132.19' (Banning address)
2020-03-14 19:25:51,319 INFO: + Added 45.143.220.240,1584140431 into blacklist again from the time: 1584140431
2020-03-14 19:25:51,319 INFO: BL: Detected attack from IP: '45.143.220.240' (Banning address)
2020-03-14 19:25:51,321 INFO: + Added 45.143.221.59,1584200178 into blacklist again from the time: 1584200178
2020-03-14 19:25:51,321 INFO: BL: Detected attack from IP: '45.143.221.59' (Banning address)
2020-03-14 19:25:51,322 INFO: + Added 192.3.140.204,1584200178 into blacklist again from the time: 1584200178
2020-03-14 19:25:51,322 INFO: BL: Detected attack from IP: '192.3.140.204' (Banning address)
2020-03-14 19:25:51,324 INFO: + Added 185.221.135.138,1584200178 into blacklist again from the time: 1584200178
2020-03-14 19:25:51,324 INFO: BL: Detected attack from IP: '185.221.135.138' (Banning address)
2020-03-14 19:25:51,326 INFO: + Added 45.143.220.25,1584200178 into blacklist again from the time: 1584200178
2020-03-14 19:25:51,326 INFO: BL: Detected attack from IP: '45.143.220.25' (Banning address)
2020-03-14 19:25:51,331 INFO: + Added 10.10.10.10 into whitelist during one year
2020-03-14 19:25:51,332 INFO: + Added 10.10.12.12 into whitelist during one year
2020-03-14 19:25:51,341 INFO: protocol version: '5.0.0'
2020-03-14 19:25:51,342 INFO: Sending awaiting actions
2020-03-14 19:47:09,842 WARNING: Received anonymous INVITE from IP 91.212.38.210
2020-03-14 20:47:14,776 INFO: TL: Expired time for 91.212.38.210
2020-03-14 21:14:17,786 WARNING: Received wrong password for user Administrator from IP 45.234.152.38
2020-03-14 21:50:28,963 WARNING: Received wrong password for user administrator from IP 45.234.152.38
2020-03-14 22:07:02,806 WARNING: Received wrong password for user 10 from IP 45.234.152.38
2020-03-14 22:14:18,490 INFO: TL: Expired time for 45.234.152.38
2020-03-14 22:24:22,969 WARNING: Received anonymous INVITE from IP 45.143.220.220
2020-03-14 22:43:22,100 WARNING: Received wrong password for user 11 from IP 45.234.152.38
2020-03-14 23:19:42,874 WARNING: Received wrong password for user 100 from IP 45.234.152.38
2020-03-14 23:24:26,489 INFO: TL: Expired time for 45.143.220.220
2020-03-14 23:27:28,488 WARNING: Received anonymous INVITE from IP 45.143.220.214
```
