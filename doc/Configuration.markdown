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
| `protocol` | Do not change this from the default. | `elemental-ircd` | string |

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

## Module-spefific configuration blocks

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

### `bot/weather`

The `weather` module needs an API key from
[WorldWeatherOnline](http://www.worldweatheronline.com/free-weather.aspx) in
order to function properly at this time. These API keys are free, but terms
of service prohibits publci distribution of them.

The API key goes in the `apikeys` block.

| Name | Descrption | Type |
|:---- |:----------- | ------:|
| `worldweatheronline` | WorldWeatherOnline API key | string |

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

