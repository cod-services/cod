package cod

type Client interface {
	Nick() string
	User() string
	Host() string
	Account() string
	Uid() string
	Permissions() int
	Umodes() int
}

type ServiceClient struct {
	nick        string
	user        string
	host        string
	VHost       string
	Ip          string
	account     string
	uid         string
	permissions int
	umodes      int
	Commands    map[string]*Command
}

func (r *ServiceClient) Nick() (string) {
	return r.nick
}

func (r *ServiceClient) User() (string) {
	return r.user
}

func (r *ServiceClient) Host() (string) {
	return r.VHost
}

func (r *ServiceClient) Account() (string) {
	return r.account
}

func (r *ServiceClient) Uid() (string) {
	return r.uid
}

func (r *ServiceClient) Permissions() (int) {
	return r.permissions
}

func (r *ServiceClient) Umodes() (int) {
	return r.umodes
}

type RemoteClient struct {
	nick        string
	user        string
	host        string
	VHost       string
	Ip          string
	account     string
	uid         string
	permissions int
	umodes      int
}

func (r *RemoteClient) Nick() (string) {
	return r.nick
}

func (r *RemoteClient) User() (string) {
	return r.user
}

func (r *RemoteClient) Host() (string) {
	return r.VHost
}

func (r *RemoteClient) Account() (string) {
	return r.account
}

func (r *RemoteClient) Uid() (string) {
	return r.uid
}

func (r *RemoteClient) Permissions() (int) {
	return r.permissions
}

func (r *RemoteClient) Umodes() (int) {
	return r.umodes
}
