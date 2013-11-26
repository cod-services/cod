cod
===

Extended IRC services and TS6 bot framework in Python

### Features:
 - Dynamic channel joins
 - Forking to background
 - Logging to snoop channel
 - Modular loading and unloading
 - No specific libc dependency (tested on glibc, uclibc and musl)
 - Rehashing config file
 - SQLite database
 - Virtual environment support

### Modules:
 - Announcing and full RBL lookups of DNSBL hits
 - DNSBL lookups to snoop channel by user or IP address
 - DNS pool displaying (Via Tortoise Labs API)
 - FAQ management
 - Forwarding of `KILL`s not made by services to snoop channel
 - JSON configuration file
 - Military operation name generation
 - MPD searching and status printing
 - Pretty printing of channel messages to the screen
 - Relaying of `HostServ` messages from snoop channel to staff channel
 - Relaying of otherwise hidden protocol abuse points to snoop channel
 - Stress testing via the Orbital Friendship Cannon

### Goals:
 - DNS record editing (Tortoise Labs)
 - MPD playlist manipulation
 - XMPP MUC linking to an existing IRC channel
 - Web GUI for administration

### Stretch Goals:
 - Automated provisioning and linking of temporary overflow IRC daemons
 - Spam filtering (opt-in only)

### Installation:
1. Set up an IRC network using Charybdis, ShadowIRCD, ponychat-ircd or any other TS6 ircd.
2. Create a link block like [this](https://gist.github.com/Niichan/9c8a8e1a1102cbee61c7).
3. Copy `etc/config.json.example` to a file of your choice.
4. Configure as needed for your deployment.
5. Run `./cod /path/to/your/config.json`
6. `@modload` the modules you want, a useful list is:

 * dnsbl
 * dnsblannounce
 * killannounce
 * relayhostserv
 * resv
 * say

The official channel for Cod is `#cod` on `irc.yolo-swag.com`. Come take
a visit and say hi!


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/lyska/cod/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

