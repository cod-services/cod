package cod

type Command struct {
	Impl   func(Client, []string)
	Uuid   string
	Script Script
	Owner  *ServiceClient
	Verb   string
	Help   string
	Perms  int
}
