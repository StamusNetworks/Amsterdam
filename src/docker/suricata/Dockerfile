FROM debian:latest

add stamus-packages.list /etc/apt/sources.list.d/
run apt-get update
run DEBIAN_FRONTEND=noninteractive apt-get install -y wget
run wget -O - -q http://packages.stamus-networks.com/packages.stamus-networks.com.gpg.key | apt-key add -
run apt-get update
run DEBIAN_FRONTEND=noninteractive apt-get install -y suricata supervisor python-pyinotify psmisc ethtool
COPY supervisor.d/* /etc/supervisor/conf.d/
COPY suri_reloader /usr/local/sbin/suri_reloader
run chmod +x /usr/local/sbin/suri_reloader
run mkdir /var/run/suricata/

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
