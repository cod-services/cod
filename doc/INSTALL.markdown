# Setup

### Dependencies:

Debian or similar:

```
$ sudo apt-get install python-dev python-pip python-virtualenv
$ sudo apt-get build-dep python-lxml
```

Alpine:

```
$ sudo apk add py-pip py-virtualenv python-dev libxml2-dev libxslt-dev
```

### Installation:

1. Set up an IRC network using Charybdis, Tethys, ShadowIRCD, Elemental-IRCd, 
   or any other TS6 daemon. If in doubt choose `charybdis` as your link 
   protocol.
2. Create a link block like [this](https://gist.github.com/lyska/9c8a8e1a1102cbee61c7).
3. Copy `etc/config.json.example` to a file of your choice. Read `Configuration.markdown`
   for more detailed explanation about each of the configuration elements.
4. Set up an account for your pesudoservice inside your IRC services package.
   This is needed at least for the automatic vhost rejection feature..
5. Configure as needed for your deployment.
6. Run `./cod /path/to/your/config.json`. By default it will use the `config.json`
   in the current working directory.
7. `@modload` the modules you want, a useful list is:

 * ctcp
 * dice
 * dnsbl
 * dnsblannounce
 * killannounce
 * killonfailoper
 * memusage
 * reddit
 * relayhostserv
   * Note that this module only works with Atheme services
 * resv
 * say
 * sendfile
 * source
 * twitchtv
 * vimeo
 * youtube

The weather script will require a free API key from [WorldWeatherOnline](http://worldweatheronline.com).

