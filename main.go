package main

import (
	"bufio"
	_ "fmt"
	"github.com/cod-services/cod/bot"
	"net/textproto"
)

func main() {
	cod := cod.NewCod()

	cod.Connect("127.0.0.1", "6667")
	defer cod.Conn.Conn.Close()

	cod.Conn.SendLine("PASS shameless TS 6 :420")
	cod.Conn.SendLine("CAPAB :QS EX IE KLN UNKLN ENCAP SERVICES EUID EOPMO")
	cod.Conn.SendLine("SERVER cod.int 1 :Cod in Go!")

	reader := bufio.NewReader(cod.Conn.Conn)
	tp := textproto.NewReader(reader)

	for {
		line, err := tp.ReadLine()
		if err != nil {
			panic(err)
		}

		cod.Conn.Log.Printf("<<< %s", line)
	}
}
