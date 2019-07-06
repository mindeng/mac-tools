# mac-tools

Tools, configs & tips for Mac.

## Software

* [oh-my-zsh](https://github.com/robbyrussell/oh-my-zsh)
* [homebrew](https://brew.sh/)
* Install vim from brew, which supports xclipboard: `brew install vim`

### Python

* python3: `brew install python`
* ipython: `pip3 install ipython`
* virtual environment: `python3 -m venv env-name`
* pycrypto: `pip3 install pycrypto`
  
## Proxy

### socks

```sh
mkdir ~/envs && cd envs
python3 -m venv ss
. ss/bin/activate
pip3 install s*s*
cat <<EOT >> ss/ss.json
{
    "server": "server_name",
    "server_port": 12345,
    "local_address": "127.0.0.1",
    "local_port": 1086,
    "password": "password",
    "timeout": 300,
    "method": "chacha20",
    "fast_open": false
}
EOT
ss -c ss/ss.json
```

### http proxy

privoxy, polipo, squid, varnish, tinyproxy
