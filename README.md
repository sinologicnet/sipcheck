<h1>SIPCheck v.3.0</h1>

## Introduction

SIPCheck is a tool that watch the authentication of users of Asterisk and bans automatically if some user (or bot) try to register o make calls using wrong passwords. 

Unlike Fail2Ban, SIPCheck manage, not just the attacker, also the clients that you have trust so if you have SIP users that has demostrated that they are trusted, it will don't ban although we receive wrong password, because it would means that lots of SIP clients behind of this IP could be banned too.

Spanish: 
Esta nueva versión cuenta con varios cambios importantes provenientes de varios usuarios que precisaban de un sistema que rechazara los ataques
pero sin expulsar a los clientes conocidos, ya que son muchos los problemas que son causados cuando un usuario de una gran empresa introduce mal
una contraseña y la antigua versión, Fail2Ban o similares, banea esa dirección IP entera expulsando a todos los usuarios que hay detrás.

Por esta razón, hemos rediseñado desde cero esta aplicación con varias ventajas con respecto a las versiones anteriores:

- Más sencillo: Más fácil de instalar, configurar y ejecutar.
- Más ligero: Orientado a grandes sistemas con un gran número de llamadas simultaneas, evitando acceder a logs y sistemas de registros.
- Persistente: Si disponemos de varias direcciones IP en la lista negra (y baneadas en el firewall), al reiniciar la aplicación, volverá a actualizarse la lista negra con todas las IPs que estuvieran y volverá a insertar en el firewall dichas IP teniendo en cuenta el tiempo en el que fueron insertadas.

## Requirements

### Python 3
SIPCheck 3 works using Python 3 and the libraries defined in `requirements.txt`

### Asterisk manager account
`/etc/asterisk/manager.conf` must have some manager user like this (change user and password variables):

```ini
[CHANGETHISUSER]
secret = CHANGETHISPASSWORD
deny = 0.0.0.0/0.0.0.0
permit = 127.0.0.1/255.255.255.255
read = security
write = system
```


## How to Install

```bash
# Download github repository
git clone https://github.com/sinologicnet/sipcheck.git /opt/sipcheck
cd /opt/sipcheck

# Install PIP for Python3
sudo apt-get install python3-pip

# Install the libraries required 
sudo pip3 install -r requirements.txt

# Copy the sample of configuration file into a official configuration file
cp sipcheck.conf.sample sipcheck.conf

# Edit this file to configure SIPCheck
nano sipcheck.conf

# Insert the script into systemd
cp /opt/sipcheck/sipcheck.service /etc/systemd/system/
systemctl enable sipcheck

# Start the application
systemctl start sipcheck

# Check if everything is working fine
tail -f /var/log/sipcheck.log
```

