package cod

import (
	"bufio"
	"github.com/cod-services/cod/1459"
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
	Handlers map[string]func(*r1459.RawLine)
	Services map[string]*ServiceClient
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
		Handlers: make(map[string]func(*r1459.RawLine)),
		Services: make(map[string]*ServiceClient),
		Bursted:  false,
	}

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
