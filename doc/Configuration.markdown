# Config blocks explained

Cod uses a json configuration file called `config.json`. There is a pre-made
example config in `etc/config.json.example`. In most cases editing this file
will suffice, but your needs may vary.

### Types of configuration elements:

| Name | Example |
|:---- | ----:|
| string | "foobang" |
| integer | 420 |
| boolean | true |

## ***REQUIRED CONFIGURATION BLOCKS***

### `me`

Basic configuration about Cod

| Name | Description | Example | Type |
|:--- |:---------- |:--- | -------:|
| `name` | TS6 pesudoserver name, must match value in C/N lines of ircd.conf | `"ardreth.shadownet.int"` | string |
| `desc` | Server description and client gecos | `"Cod fishy"` | string |
| `nick` | Pseudoclient nick | `"Cod"` | string |
| `user` | ident of pesudoclient | `"fish"` | string |
| `host` | vhost of pseudoclient | `blub.blub` | string |
| `servicespass` | NickServ password of pesudoclient. Make this complicated and hard to guess | `"yoloswag420"` | string |
| `prefix` | Channel command prefix, suggested to be `@` or `;`. Will not work if more than one character | `"@"` | string |
| `netname` | The name of your network. | `ShadowNET` | string |
| `motd` | MOTD message for a remote /MOTD | `"etc/cod.motd"` | string |
| `dbpath` | path to the SQLite database that Cod uses internally | `"var/cod.db"` | string |

### `uplink`

Information about the uplink ircd

| Name | Description | Example | Type   |
|:---- |:----------- |:------- | ------:|
| `host` | Hostname of the uplink ircd | `"127.0.0.1"` | string |
| `port` | Portnumber to connect to | `6667` | integer |
| `pass` | Password to send to the remote ircd | `"dev"` | string |
| `ssl` | If we are supposed to connect over SSL | `false` | boolean |
| `protocol` | What protocol is being used. | `elemental-ircd` | string |

### `etc`

Various other settings

| Name | Description | Example | Type   |
|:---- |:----------- |:------- | ------:|
| `debug` | Whether or not to log/print all lines sent to and recieved from the server. Don't enable in production. | `false` | boolean |
| `production` | Whether or not to fork to the background | `true` | boolean |
| `snoopchan` | The channel that Cod will log all administrative actions or unexpected exceptions to | `"#services"` | string |
| `staffchan` | The channel that Cod will send relayed HostServ messages to or other notifications about operator actions. | `"#opers"` | string |
| `helpchan` | The network help channel name | `"help"` | string |
| `logfile` | The file that cod will log to | `"var/cod.log"` | string |
| `contrib` | Wether or not to use contrib modules | `true` | boolean|

## Module-spefific configuration blocks

Some modules need to add configuration keys to existing blocks. The shorthand
syntax `level::name` expands to:

```javascript
"level": {
	"name": "foo"
}
```

### `bot/mpdclient`

The `mpdclient` module uses a `mpd` block for its configuration parameters.

| Name | Description | Type |
|:---- |:----------- | ------:|
| `host` | MPD server to connect to | string |
| `port` | Port that MPD is listening on | integer |

Example:

```javascript
"mpd": {
    "host": "127.0.0.1",
    "port": 6600
},
```

### `bot/opname`

The `opname` module needs prefix and suffix files, which conveniently are
shipped in every base distribution of Cod. The `services/ofc` module also uses
these files.

| Name | Description | Example | Type |
|:---- |:----------- |:------- | ----:|
| `etc::prefixfile` | List of prefixes for the military operation name generator | `"etc/prefix.txt"` | string |
| `etc::suffixfile` | List of suffixes for the military operation name generator | `"etc/suffix.txt"` | string |

### `bot/weather`

The `weather` module needs an API key from
[WorldWeatherOnline](http://www.worldweatheronline.com/free-weather.aspx) in
order to function properly at this time. These API keys are free, but terms
of service prohibits publci distribution of them.

The API key goes in the `apikeys` block.

| Name | Descrption | Example | Type |
|:---- |:---------- |:------- | ----:|
| `apikeys::worldweatheronline` | WorldWeatherOnline API key | `"asdfewsdf"` | string |

### `services/faq`

The `faq` module defines its own pesudoclient. As such it needs to have information
set about it.

| Name | Description | Type |
|:---- |:----------- | ------:|
| `nick` | Nickname for FAQ client | string |
| `user` | Ident for FAQ client | string |
| `host` | Vhost for FAQ client | string |
| `gecos` | Realname for FAQ client | string |

Example:

```javascript
"faq": {
    "nick": "FAQServ",
    "user": "faq",
    "host": "services.example.com",
    "gecos": "FAQ Service"
},
```

#### `services/autocloak`

`autocloak` allows administrators to specify specific IP addresses that are 
bouncer hosts and to apply a randomly generated vhost on connect.

As this is a pesudoclient-introducing module, it requires a nick, user, gecos 
and host configuration as well as the list of bouncers.

An example using `bnc.im` and IRCCloud's public IP addresses is shown below:

```javascript
    "autocloak": {
        "nick": "Gatekeeper",
        "user": "guardian",
        "host": "services.example.com",
		"gecos": "The gatekeeper",

		"list": {
			"172.246.127.154": "bnc.im",
			"172.246.127.176": "bnc.im",
			"172.246.127.177": "bnc.im",
			"172.246.127.178": "bnc.im",
			"172.246.127.179": "bnc.im",
			"88.150.203.213": "bnc.im",
			"88.150.203.196": "bnc.im",
			"198.52.200.15": "bnc.im",
			"198.52.200.16": "bnc.im",
			"198.52.199.84": "bnc.im",
			"198.52.199.85": "bnc.im",
			"213.138.108.24": "bnc.im",
			"213.138.108.247": "bnc.im",
            "192.184.9.108": "irccloud.com",
			"192.184.9.110": "irccloud.com",
			"192.184.9.112": "irccloud.com",
			"192.184.9.114": "irccloud.com"
		}
	},

```


