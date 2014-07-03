package cod

type Script interface {
	GetCommands() []*Command
	AddCommand(verb string, perms int, help string, impl func (*Client, []string)) (error)
	DelCommand(*Command) (error)
	AddHandler(verb string) (error)
	DelHandler(*Handler) (error)
}

