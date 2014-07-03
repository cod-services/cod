package main

import (
	"github.com/cod-services/cod/bot"
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

		cod.Conn.Log.Printf("<<< %s", line)
	}
}
