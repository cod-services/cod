package main

import (
	"github.com/cod-services/cod/bot"
	"fmt"
	"bufio"
	"net"
	"net/textproto"
)

func main() {
	var connection *cod.Connection
	connection = new(cod.Connection)

	var err error
	connection.Conn, err = net.Dial("tcp", "127.0.0.1:6667")
	if err != nil {
		panic(err) // We should an hero here
	}

	defer connection.Conn.Close()

	fmt.Fprintln(connection.Conn, "PASS shameless TS 6 :420")
	fmt.Fprintln(connection.Conn, "CAPAB :QS EX IE KLN UNKLN ENCAP SERVICES EUID EOPMO")
	fmt.Fprintln(connection.Conn, "SERVER cod.int 1 :Cod in Go!")

	reader := bufio.NewReader(connection.Conn)
	tp := textproto.NewReader(reader)

	for {
		line, err := tp.ReadLine()
		if err != nil {
			panic(err)
		}

		fmt.Printf("%s\n", line)
	}
}

