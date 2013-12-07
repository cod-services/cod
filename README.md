Cod
===

Extended IRC services in Python

[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/lyska/cod/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

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
 - Brainfuck interpreter
 - DNSBL lookups to snoop channel by user or IP address
 - DNS pool displaying (Via Tortoise Labs API)
 - FAQ management
 - Fibbonacci number lookups
 - Forwarding of `KILL`s not made by services to snoop channel
 - Gentle reminders for people that use "nick|away" nicknames
 - Immature phrase appender
 - JSON configuration file
 - Kill clients on a failed `OPER` attempt and log to snoop channel
 - Military operation name generation
 - Memory use statistics
 - MPD interface
   - Pause/Play/Next/Previous
 - Partial inspircd support (If you know anything about the inspircd link protocol,
   help would really be appreciated)
 - Pretty printing of channel messages to the screen or log file
 - Relaying of `HostServ` messages from snoop channel to staff channel
   - Also does `HostServ` lookups on requested vhosts
 - Relaying of otherwise hidden protocol staff abuse points to snoop channel
   - On elemental-ircd, DNSBL hits are logged
   - `RESV` use
 - SQLite database
 - Sending files from the disk to a user or channel
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
1. Set up an IRC network using Charybdis, ShadowIRCD, elemental-ircd or any other
   TS6 ircd. Note that regardless of what TS6 irc daemon you end up choosing,
   your protocol module will have to be `elemental-ircd`.
2. Create a link block like [this](https://gist.github.com/lyska/9c8a8e1a1102cbee61c7).
3. Copy `etc/config.json.example` to a file of your choice.
4. Set up an account for your pesudoservice inside your IRC services package.
   This is needed for the automatic vhost rejection feature as well as many
   others waiting to be written.
5. Configure as needed for your deployment.
6. Run `./cod /path/to/your/config.json`. By default it will use the `config.json`
   in the current working directory.
7. `@modload` the modules you want, a useful list is:

 * dnsbl
 * dnsblannounce
 * killannounce
 * killonfailoper
 * memusage
 * relayhostserv
 * resv
 * say
 * sendfile

The official channel for Cod is `#cod` on `irc.yolo-swag.com`. Come take
a visit and say hi!

