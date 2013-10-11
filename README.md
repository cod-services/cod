cod
===

Extended IRC services and TS6 bot framework in Python

Features:
 - DNSBL lookups to snoop channel by user or IP address
 - Forwarding of `KILL`s not made by services to snoop channel (`#services`)
 - Logging to snoop channel (`#services`)
 - Forking to background
 - Rehashing config file
 - Dynamic channel joins
 - Military operation name generation

Goals:

 - DNS record editing (Tortoise Labs)
 - DNSBL lookups (the dynamic and spam ones) on user join and log to snoop channel
 - Forwarding of `KILL`s not made by services to snoop channel (`#services`)
 - Logging to snoop channel (`#services`)
 - MPD playlist manipulation
 - RemindServ
 - XMPP MUC linking to an existing IRC channel
 - Web GUI for administration

Stretch Goals

 - Automated provisioning and linking of temporary overflow IRC daemons
 - Spam filtering (opt-in only)
