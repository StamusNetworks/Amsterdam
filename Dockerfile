#
# Amsterdam (SELKS) in Docker.
#
# We need access to the host's Docker socket, so run the container like so:
#
#     - docker build -t amsterdam .
#     - docker run --rm -v /var/run/docker.sock:/var/run/docker.sock amsterdam
#

FROM python:2-alpine

# Alpine packages to install.
ENV APK_PACKAGES \
    alpine-sdk \
    libffi-dev \
    openssl-dev \
    tzdata \
    git

# PyPI packages to install.
ENV PIP_PACKAGES \
    docker \
    docker-compose \
    six \
    cryptography \
    pyopenssl

# Install above packages.
RUN apk --no-cache add $APK_PACKAGES
RUN pip install $PIP_PACKAGES

# Configure the system time.
RUN apk add tzdata && \
    cp /usr/share/zoneinfo/Europe/London /etc/localtime && \
    echo "Europe/London" > /etc/timezone && \
    apk del tzdata

# Clone the Amsterdam repo.
RUN git clone https://github.com/StamusNetworks/Amsterdam.git /opt/Amsterdam/

# Build & install Amsterdam from source.
WORKDIR /opt/Amsterdam/
RUN sudo python setup.py install

ENTRYPOINT ["amsterdam"]
