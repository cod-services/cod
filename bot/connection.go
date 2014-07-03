package cod

import (
	"fmt"
	"log"
	"net"
	"os"
)

type Connection struct {
	Conn          net.Conn
	Log           *log.Logger
}

func NewConnection() (c *Connection) {
	c = &Connection{
		Log: log.New(os.Stdout, "LINK ", log.LstdFlags),
	}

	return
}

func (c *Connection) SendLine(line string, stuff... interface{}) {
	log.Printf(">>> " + line, stuff...)
	fmt.Fprintf(c.Conn, line + "\r\n", stuff...)
}

