FROM debian

add stamus-packages.list /etc/apt/sources.list.d/
run apt-get update
run DEBIAN_FRONTEND=noninteractive apt-get install -y wget
run wget -O - -q http://packages.stamus-networks.com/packages.stamus-networks.com.gpg.key | apt-key add -
run apt-get update
run DEBIAN_FRONTEND=noninteractive apt-get install -y suricata

ENTRYPOINT ["/usr/bin/suricata"]
