package cod

import (
	"code.google.com/p/go-uuid/uuid"
	"github.com/cod-services/cod/1459"
)

type Handler struct {
	Impl func(*r1459.RawLine)
	Verb string
	Uuid string
}

func (cod *Cod) AddHandler(verb string, impl func(*r1459.RawLine)) (handler *Handler, err error) {
	handler = &Handler {
		Verb: verb,
		Impl: impl,
		Uuid: uuid.New(),
	}

	if _, ok := cod.Handlers[verb]; !ok {
		cod.Handlers[verb] = make(map[string]*Handler)
	}

	cod.Handlers[verb][handler.Uuid] = handler

	return
}

