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

