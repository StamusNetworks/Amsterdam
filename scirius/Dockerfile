FROM debian

ENV VERSION 1.1
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y wget python-pip python-dev
ADD stamus-packages.list /etc/apt/sources.list.d/
RUN wget -O - -q http://packages.stamus-networks.com/packages.stamus-networks.com.gpg.key | apt-key add -
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y suricata git
WORKDIR /tmp/
RUN wget https://github.com/StamusNetworks/scirius/archive/scirius-${VERSION}.tar.gz
RUN mkdir -p /opt/selks/
WORKDIR /opt/selks
RUN tar zxf /tmp/scirius-${VERSION}.tar.gz
RUN ln -sf /opt/selks/scirius-scirius-${VERSION} /opt/selks/scirius
WORKDIR /opt/selks/scirius
RUN pip install -r requirements.txt
RUN ln -s /etc/scirius/local_settings.py /opt/selks/scirius/scirius/
RUN echo "no" | python manage.py syncdb
ADD django/scirius.json /tmp/
RUN python manage.py loaddata /tmp/scirius.json
RUN python manage.py migrate
RUN python manage.py createcachetable my_cache_table

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
