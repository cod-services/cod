package cod

import (
	"os"
	"log"
	"bufio"
	"net"
	"net/textproto"
)

type Clients struct {
	ByNick map[string]*Client
	ByUID  map[string]*Client
}

type Cod struct {
	Conn    *Connection
	Info    *Server
	Clients *Clients
	Bursted bool
	//Config *Config
}

func NewCod() (cod *Cod) {
	cod = &Cod{
		Conn: &Connection {
			Log: log.New(os.Stdout, "LINK ", log.LstdFlags),
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
