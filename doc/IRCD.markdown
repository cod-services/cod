# IRCd configuration

## Charybdis or Elemental-IRCd

Cod links like any other services server except no `hub_mask` is needed at this 
time. Cod may also link over SSL. Note that your experience may be better with 
Elemental-IRCd.

```
connect "cod.int" {
	host = "127.0.0.1";
    send_password = "dev";
	accept_password = "dev";
	port = 6667;
	class = "server";
};

service {
    name = "cod.int";
};
```

## Tethys

Tethys configuration subject to change without notice.

```
link cod.int {
    host = "127.0.0.1";
    sendpass = "dev";
    recvpass = "dev";
    class = "server";
};
```

