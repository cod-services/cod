package cod

type ChanUser struct {
	Client  *Client
	Channel *Channel
	Prefix  int
}

type Channel struct {
	Name    string
	Ts      int64
	Modes   int
	Clients map[string]*ChanUser
	Lists   map[string][]string
}

func NewChannel(name string, ts int64) (c *Channel) {
	c = &Channel{
		Name:  name,
		Ts:    ts,
		Lists: make(map[string][]string),
	}

	return
}
