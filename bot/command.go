package cod

type Command struct {
	Impl  func(Client, []string)
	Uuid  string
	Owner *ServiceClient
	Verb  string
	Help  string
	Perms int
}
