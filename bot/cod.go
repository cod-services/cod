package cod

import (
	"net"
)

type Clients struct {
	ByNick map[string]*Client
	ByUID  map[string]*Client
}

type Cod struct {
	Conn *Connection
	Info *Server
	Clients *Clients
	//Config *Config
}

func NewCod() (cod *Cod) {
	cod = &Cod{
		Conn: NewConnection(),
		Info: &Server {
			Name: "cod.int",
			Sid:  "420",
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
	cod.Conn.Conn, err = net.Dial("tcp", host + ":" + port)
	if err != nil {
		panic(err)
	}

	return
}

func (cod *Cod) GetConn() (*net.Conn) {
	return &cod.Conn.Conn
}

