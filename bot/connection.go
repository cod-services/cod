package cod

import (
	"log"
	"net"
	_ "net/textproto"
)

type Connection struct {
	Conn          *net.Conn
	Log           *log.Logger
	Link          *Server
	ClientsByUID  map[string]*Client
	ClientsByNick map[string]*Client
	Host          string
	Port          string
}


