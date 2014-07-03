package main

import (
	_ "fmt"
	"github.com/cod-services/cod/bot"
	"github.com/cod-services/cod/1459"
)

func main() {
	cod := cod.NewCod()

	cod.Connect("127.0.0.1", "6667")
	defer cod.Conn.Conn.Close()

	cod.Conn.SendLine("PASS shameless TS 6 :420")
	cod.Conn.SendLine("CAPAB :QS EX IE KLN UNKLN ENCAP SERVICES EUID EOPMO")
	cod.Conn.SendLine("SERVER cod.int 1 :Cod in Go!")

	for {
		line, err := cod.Conn.GetLine()
		if err != nil {
			panic(err)
		}

		rawline := r1459.NewRawLine(line)

		cod.Conn.Log.Printf("<<< %s", line)

		if rawline.Verb == "PING" {
			cod.Conn.SendLine("PONG :%s", rawline.Args[0])
		}
	}
}
