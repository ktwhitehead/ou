# ou

netsh interface portproxy add v4tov4 listenport=3001 listenaddress=192.168.68.101 connectport=3001 connectaddress=192.168.145.182
netsh interface portproxy add v4tov4 listenport=5000 listenaddress=192.168.68.101 connectport=5000 connectaddress=192.168.145.182

sudo kill -9 `sudo lsof -t -i:5000`