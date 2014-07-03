package cod

import (
	"github.com/cod-services/cod/1459"
	"bufio"
	"log"
	"net"
	"net/textproto"
	"os"
)

type Clients struct {
	ByNick map[string]*Client
	ByUID  map[string]*Client
}

type Cod struct {
	Conn     *Connection
	Info     *Server
	Clients  *Clients
	Bursted  bool
	Handlers map[string]map[string]*Handler
	Services map[string]*ServiceClient
	Servers  map[string]*Server
	//Config *Config
}

func NewCod() (cod *Cod) {
	cod = &Cod{
		Conn: &Connection{
			Log: log.New(os.Stdout, "", log.LstdFlags),
		},
		Info: &Server{
			Name:  "cod.int",
			Sid:   "420",
			Gecos: "Cod in Go!",
		},
		Clients: &Clients{
			ByNick: make(map[string]*Client),
			ByUID:  make(map[string]*Client),
		},
		Handlers: make(map[string]map[string]*Handler),
		Services: make(map[string]*ServiceClient),
		Servers:  make(map[string]*Server),
		Bursted:  false,
	}

	cod.AddHandler("EUID", func (line *r1459.RawLine) {
		// :47G EUID xena 1 1404369238 +ailoswxz xena staff.yolo-swag.com 0::1 47GAAAABK 0::1 * :Xena
		nick := line.Args[0]
		user := line.Args[4]
		host := line.Args[5]
		ip := line.Args[10]
		uid := line.Args[9]

		client := &RemoteClient {
			nick: nick,
			user: user,
			VHost: host,
			host: line.Args[6],
			uid: uid,
			Ip: ip,
			account: line.Args[11],
		}

		cod.Clients.ByNick[nick] = *Client(client)
		cod.Clients.ByUID[uid] = *Client(client)
	})

	return
}

func (cod *Cod) Connect(host, port string) (err error) {
	cod.Conn.Conn, err = net.Dial("tcp", host+":"+port)
	if err != nil {
		panic(err)
	}

	cod.Conn.Reader = bufio.NewReader(cod.Conn.Conn)
	cod.Conn.Tp = textproto.NewReader(cod.Conn.Reader)

	return
}

func (cod *Cod) GetConn() *net.Conn {
	return &cod.Conn.Conn
}
