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

## InspIRCd

Cod requires the same InspIRCd modules that Atheme does. An example 
configuration for linking InspIRCd to Cod is shown below:

```
<uline server="cod.int">

<link name="cod.int"
      ipaddr="localhost"
      port="7001"
      allowmask="127.0.0.0/8"
      sendpass="password"
      recvpass="password">

#Absolutely required.
<module name="m_spanningtree.so">
<module name="m_services_account.so">
<module name="m_servprotect.so">
<module name="m_chghost.so">

# Needed for SVSOPER
<module name="m_svsoper.so">
```

