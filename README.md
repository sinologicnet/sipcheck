<h1>SIPCheck</h1>

<h2>Goal</h2>
The project's goal is get a tool that continuously check if our Asterisk system are the victim of an attack,
gather the IP addresses of the attackers and publish them if they return or are dangerous.

<h2>Parts of the project</h2>
<ul>
    <li>Asterisk module that execute the checker each X times.</li>
    <li>Parser that checks in Asterisk logs if we are victims of an attack.</li>
    <li>Counter attacking system and karma manager in the firewall and the server.</li>
    <li>...</li>
</ul>

# TODO
*  Enable IPv6 support
* Control logrotate to reopen log file
