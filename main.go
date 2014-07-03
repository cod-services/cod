package main

import (
	"bufio"
	"fmt"
	"github.com/cod-services/cod/bot"
	"net/textproto"
)

func main() {
	cod := cod.NewCod()

	cod.Connect("127.0.0.1", "6667")
	defer cod.Conn.Conn.Close()

	fmt.Fprintln(cod.Conn.Conn, "PASS shameless TS 6 :420")
	fmt.Fprintln(cod.Conn.Conn, "CAPAB :QS EX IE KLN UNKLN ENCAP SERVICES EUID EOPMO")
	fmt.Fprintln(cod.Conn.Conn, "SERVER cod.int 1 :Cod in Go!")

	reader := bufio.NewReader(cod.Conn.Conn)
	tp := textproto.NewReader(reader)

	for {
		line, err := tp.ReadLine()
		if err != nil {
			panic(err)
		}

		fmt.Printf("%s\n", line)
	}
}
