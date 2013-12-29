# Modules shipped with Cod

The modules in Cod are separated into seven types:

| Type | Description |
|:---- |:----------- |
| `announcer` | Modules that listen for protocol/services events and announce them to operators. |
| `bot` | Pseudoclient commands for users. |
| `core` | Core functionality for administrators and users. |
| `experimental` | Normally untracked in git, this is a place to store local, experimental modules while they are being written until they can be comitted proper. |
| `protocol` | Protocol modules to have Cod talk over different server to server protocols. This is currently used only for the TS6 protocol handler, but is available for future expansion. |
| `scrapers` | Handles scraping PRIVMSG lines for links it can parse out and parses them, returning it to the channel. |
| `services` | Other pesudoservices that Cod introduces or handlers for Atheme/Anope integration. |

## `announcer`

#### `awayreminder`

Scans nickchanges to look for nicknames that are what some clients automatically
postpend to people marked as away, and reminds them to not use them.

#### `dnsblannounce`

***THIS MODULE ONLY WORKS WITH ELEMENTAL-IRCD BECAUSE OF A MODIFICATION IN IT MAKING DNSBL HITS GLOBAL SERVER NOTICES***

Scans the incoming server to server notices for a rejection notice because of a
DNSBL hit, then checks the offending address against many DNS blacklists, sending
the results to the services snoop channel.

Example:

```
@Cod | DNSBL:HIT: TorUser1 (TorUser1@198.96.155.3) is being disconnected due to being listed in DNS Blacklist rbl.efnetrbl.org
@Cod | Checking 198.96.155.3 in 83 blacklists...
@Cod |  + Additional information: TOR Server detected - see http://www.sectoor.de/tor.php for more information.
@Cod |  + Additional information: Blocked - see http://cbl.abuseat.org/lookup.cgi?ip=198.96.155.3
```

#### `killannounce`

Logs oper kills to the services snoop channel.

#### `prettyprint`

Logs all the channel PRIVMSG's it can see to the logfile cleanly.

#### `relayhostserv`

Relays all HostServ messages to the staff channel, automatically rejects real
domain names with a note to visit the help channel, and automatically does
vhost lookups so that opers can reject similar ones easily.

#### `resvannounce`

Announces RESV use and logs it.

## `bot`

| Name | Command | Oper-only? | Description |
|:---- |:------- |:---------- |:----------- |
| `bf` | `BF` | No | A simple brainfuck interepreter for one-line experimentation. |
| `btc` | `BTC` | No | Grabs the latest prices from MTGox. |
| `choice` | `CHOICE` | No | Randomly chooses from a list of one or more comma-seperated choices. |
| `dice` | `DICE` | No | Simulates dice rolls |
| `dnsbl` | `RBL` | Yes | Does DNSBL lookups on arbitrary users or IP addresses. |
| `fibbonacci` | `FIB` | No | A memoizing fibbonacci calculator. |
| `fpdtest` | `FPDTEST` | Yes | A flash policy daemon tester. |
| `immature` | `IMMATURE` | No | A smart immature phrase appender. |
| `memusage` | `MEM` | Yes | Shows memory usage statistics. |
| `mpdclient` | `MPD` | Some parts | A simple MPD client, shows currently playing song and lets opers control next/previous. |
| `opname` | `OPNAME` | No | Bad 80's B-movie style military operation name generator. |
| `ponify` | `PONIFY` | No | Makes text easy to read so everypony can understand it by removing all those weird "human" terms. |
| `say` | `SAY` | Yes | Lets an oper have the main client send arbitrary text to an arbitrary channel or user. |
| `sendfile` | `SENDFILE` | Yes | Lets an oper send the contents of a text file to a user or channel. Useful in sharing ascii art. |
| `shibe` | `SHIBE` | No | Generates shibe text from user input. |
| `tfw` | `TFW` | No | Does weather lookups from http://thefuckingweather.com |
| `weather` | `WEATHER` | No | Does weather lookups via http://worldweatheronline.com (API key needed, see configuration document). |
| `whoami` | `WHOAMI` | No | Shows what Cod knows about you. |

## `core`

#### `admin`

| Command | Description |
|:------- |:----------- |
| `JOIN` | Makes Cod join a channel and remember it. This does not check bans. |
| `PART` | Makes Cod part a channel and forget to join it. |
| `REHASH` | Re-reads the configuration file. |
| `DIE` | Kills Cod. |
| `MODLOAD` | Loads a module and adds it to the autoload if sucessful. |
| `MODUNLOAD` | Unloads a module and deletes it from the autoload. |
| `LISTCHANS` | Notices the list of autojoins. |
| `VERSION` | Replies with what version the Cod core thinks it is. |
| `UPGRADE` | Uses git to pull the latest updates. Does not reload anything. |

#### `help`

Shows what commands are available to opers and users. Oper-only commands will
not show up to users and are surrounded by parentheses.

## `scrapers`

| Name | Site to scrape | Description |
|:---- |:-------------- |:----------- |
| `4chan` | http://4chan.org | Grabs OP name and first line of a post from 4chan. |
| `danbooru` | http://danbooru.donmai.us | Grabs the tags and SFW-ness of a link from Danbooru. |
| `derpibooru` | http://derpibooru.org | Grabs the tags and SFW-ness of a link from Derpibooru. |
| `eqbeats` | http://eqbeats.org | Grabs artist and track name of a link from EQBeats. |
| `reddit` | http://reddit.com | Grabs the name and link (if applicable) of a post on reddit. |
| `soundcloud` | http://soundcloud.com | Grabs the artist and title of a song from soundcloud. |
| `twitchtv` | http://twitch.tv | Grabs the stream info from a twitch.tv stream. |
| `youtube` | http://youtube.com | Grabs youtube video information and defines a simple search command `YT` |

## `services`

| Name | Description |
|:---- |:----------- |
| `faq` | Stores and spits out FAQ entries. |
| `funservjoin` | Listens for FunServ commands to join channels and gives users information about how to use Cod as a bot. |
| `ofc` | The Orbital Friendship Cannon. A stress tester. See `OFC HELP` for usage. |

