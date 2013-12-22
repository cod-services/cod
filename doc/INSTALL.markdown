# Setup

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
 * help
 * killannounce
 * killonfailoper
 * memusage
 * relayhostserv
 * resv
 * say
 * sendfile
 * twitchtv
 * youtube

The weather script will require an API key from [WorldWeatherOnline](http://worldweatheronline.com).

