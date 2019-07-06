# mac-tools

Tools, configs & tips for Mac.

## Configs

```sh
git clone git@github.com:mindeng/mac-tools.git && cd mac-tools
python3 ./mac-init.py
```

## Tools

* [oh-my-zsh](https://github.com/robbyrussell/oh-my-zsh)
* [homebrew](https://brew.sh/)
* Install vim from brew, which supports xclipboard: `brew install vim`

### Python

```sh
brew install python
pip3 install ipython
pip3 install pycrypto
brew install pipenv
```

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

## privoxy

```sh
brew install privoxy
cat <<EOT >> /usr/local/etc/privoxy/config
forward-socks5t / 127.0.0.1:1086 .
EOT
brew services start privoxy
```

default listen address: 127.0.0.1:8118