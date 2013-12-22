Cod
===

Extended IRC services in Python [![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/lyska/cod/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

Installation directions are in `doc/INSTALL.markdown`. Directions for setting
up Atheme integration are in `doc/funserv.markdown`. If you have any questions,
please ask in `#cod` on `irc.yolo-swag.com`.

### Features:
 - Asynchronous socket handling
   (and an easy way for modules to add socket handlers)
 - Dynamic channel joins
 - Forking to background
 - Logging to snoop channel
 - Modular loading and unloading
 - No specific libc dependency (tested on glibc, uclibc and musl)
 - Rehashing config file
 - Separation of user and oper commands
 - SQLite database
 - TS6 link protocol support
 - Virtual environment support

### Modules:
 - Announcing and full RBL lookups of DNSBL hits (on elemental-ircd only)
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
 - Pretty printing of channel messages to the screen or log file
 - Random choice from a list
 - Relaying of `HostServ` messages from snoop channel to staff channel
   - Also does `HostServ` lookups on requested vhosts
   - Automatically rejects real domain names
 - Relaying of otherwise hidden protocol staff abuse points to snoop channel
   - On elemental-ircd, DNSBL hits are logged
   - `RESV` use
 - SQLite database
 - Sending files from the disk to a user or channel
 - Stress testing via the Orbital Friendship Cannon
   - Statistics logging of OFC runs

### URL Scraping:
 - 4chan post lookups
 - danbooru post lookups
 - derpibooru post lookups
 - reddit post lookups
 - Twitch.tv API lookups of video streams
 - Youtube API lookups and searching

### Goals:
 - DNS record editing (Tortoise Labs)
 - Feature-completeness with skybot
 - MPD playlist manipulation
 - User statistics collection
   - Follow anonyminity standards of the Tor Project
 - Web GUI for administration

### Stretch Goals:
 - Automated provisioning and linking of temporary overflow IRC daemons
 - Spam filtering (opt-in only)

The official channel for Cod is `#cod` on `irc.yolo-swag.com`. Come take
a visit and say hi!

