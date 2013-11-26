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

Installing the applicacion:
<pre>cd sipcheck
python setup.py install
</pre>

We could get new user account to use shared lists.

Modify configuration file to customize it.

Execute the application
<pre>./bin/sipcheck -c ./etc/sipcheck.conf</pre>

<h2>TODO</h2>
*  Enable IPv6 support
