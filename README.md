<h1>SIPCheck v.3.0</h1>

## Introduction

El objetivo de SIPCheck es el de vigilar para evitar ataques de bots y usuarios maliciosos en nuestros sistemas Asterisk.

Esta nueva versión cuenta con varios cambios importantes provenientes de varios usuarios que precisaban de un sistema que rechazara los ataques
pero sin expulsar a los clientes conocidos, ya que son muchos los problemas que son causados cuando un usuario de una gran empresa introduce mal
una contraseña y la antigua versión, Fail2Ban o similares, banea esa dirección IP entera expulsando a todos los usuarios que hay detrás.

Por esta razón, hemos rediseñado desde cero esta aplicación con varias ventajas con respecto a las versiones anteriores:

- Más sencillo: Más fácil de instalar, configurar y ejecutar.
- Más ligero: Orientado a grandes sistemas con un gran número de llamadas simultaneas, evitando acceder a logs y sistemas de registros.


## Requirements

Tan solo es necesario disponer de Python 3 y las librerías definidas en el archivo `requirements.txt`

`/etc/asterisk/manager.conf` must have some manager user like this (change user and password variables):

```
[CHANGETHISUSER]
secret = CHANGETHISPASSWORD
deny = 0.0.0.0/0.0.0.0
permit = 127.0.0.1/255.255.255.255
read = security
write = system
```


## How to Install




Debian Stretch:
```bash
# Download github repository
cd /opt
git clone https://github.com/sinologicnet/sipcheck.git sipcheck
cd sipcheck

# Install PIP for Python3
sudo apt-get install python3-pip

# Install the libraries required 
sudo pip3 install -r requirements.txt

# Important: Edit sipcheck.py file and modify the configuration variables as your needed
nano sipcheck.py

# Execute
./sipcheck.py
```

If you want to install into your system as a service:

```bash
cp /opt/sipcheck/sipcheck.service /etc/systemd/system/
systemctl enable sipcheck
systemctl start sipcheck
```
