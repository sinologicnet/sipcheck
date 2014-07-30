<h1>SIPCheck</h1>

<h2>Goal</h2>

<p>
The purpose of this application is to serve as a "watchdog" of an Asterisk system so that it can detect attempted 
attacks and update the firewall rules to prevent further attack.
When an attack is detected, the application will inform Sinologic.net to introduce the attacker in a public list 
to report to other users who use this application and can ban IP addresses that attackers always considered a real 
danger and thus preempt to attack.
</p>

<h2>How it works</h2>
<p>
The operation is very simple, sipcheck, once configured, will parse the file 'messages' Asterisk for lines that show attempts to attack:
</p>
<p>
[show some examples]
<p>
Once it has identified a number of attempts from the same IP address, the system will activate the defense system:
<ul>
    <li>Activating the shields (entering the IP address in the firewall)</li>
    <li>Spreading the information (sending that IP address to Sinologic)</li>
    <li>Sending countermeasures (running a specific code when it detects an attacker IP)</li>
</ul>

<h2>Instalation</h2>

Downloading the application:
<pre>git clone https://github.com/sinologicnet/sipcheck</pre>

Sure yourself have installed <strong>python-setuptools</strong> package before to continue.

Installing the applicacion:
<pre>cd sipcheck
python setup.py install
</pre>
<p>
We could get new user account to use shared lists.<br />
<br />
When you use a shared list features, you will need a "key user" that you will configure into configuration file.<br />
This "key" will be used for ranking and fiability of the ips reported.<br />
During the beta version time, you can get your "temporal key" entering in this page:<br />
  <a href="http://sipcheck.sinologic.net/getKey">http://sipcheck.sinologic.net/getKey</a>
<br />
Although you can set "key" field as anonymous we recommend that register and use your own key.<br />
</p>



<h2>Configuration</h2>
You need customize sipcheck application:
<pre>
[general]
messagefile=/var/log/asterisk/messages      ; Asterisk message file. Sure you that you log errors
loglevel=debug                              ; 
useiptables=True                            ; If you want insert into iptables.
minticks=5                                  ; Num of try before consider an attack
logfile=/tmp/sipcheck.log                   ; Log file

[shared]
enable=True                                 ; Enable this if you want to report attackers to a common list
key=494949                                  ; Personal KEY

[database]
file=/tmp/sipcheck.db                       ; Local database where all information is storaged

[ignore]                                    ; List of host and network to ignored if they are detected as attackers
own=178.60.201.227/32,127.0.0.1/32,192.168.0.0/16,10.0.0.0/12

[gui]                                       ; On construction... 
enable=True
port=8081
user=admin
pass=sipcheck
listen=127.0.0.1
</pre>

Execute the application
<pre>./bin/sipcheck -c ./etc/sipcheck.conf</pre>

<h2>TODO</h2>
*  Enable IPv6 support


<h2>Credits</h2>
<h3>Developers</h3>
<ul>
    <li>Elio Rojano</li>
    <li>Sergio Cotelo</li>
    <li>Tomás Sahagún</li>
    <li>Javier Vidal</li>
</ul>
<h3>Helpers, Colaborators and Supporters</h3>
<ul>
    <li>Saúl Ibarra > @saghul</li>
    <li>Juan García > @ramses-0000</li>
    <li>Rosa Atienza</li>
</ul>
