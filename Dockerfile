FROM ubuntu:bionic

RUN apt-get update && apt-get upgrade -y -o Dpkg::Options::="--force-confold"
RUN apt-get install -y software-properties-common
# GPG from ubuntu-mate-dev repository
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys FB01CC26162506E7
RUN apt-add-repository "deb http://ppa.launchpad.net/ubuntu-mate-dev/ppa/ubuntu trusty main "
# RUN add-apt-repository ppa:chris-lea/libsodium
RUN apt-get update

# Minimum Gnome environment
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install \
  --no-install-recommends xvfb ubuntu-mate-core ubuntu-mate-desktop

# Required for TCNode in dogtail
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install \
    libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev \
    liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev \
    libatk-adaptor libgail-common

# Python env for dogtail
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install \
    --no-install-recommends python python3-pip python-gobject \
    python-dev python3-setuptools python3-pil python3-wheel \
    python3-cairo python3-pyatspi

# Pidgin
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install \
    --no-install-recommends libpurple-dev pidgin-dev

# Tools for compiling libotr-ng and libgoldilocks
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install \
   --no-install-recommends git autoconf libtool libsodium-dev \
    libotr5-dev automake libgcrypt20 libglib2.0-dev intltool \
    gtk2.0 libxml2-dev

# Enable remote debugging with x11vnc
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install x11vnc
EXPOSE 5900

# Clean up APT when done.
# RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

VOLUME /src
VOLUME /tmp/dogtail-root

ADD . /src
ADD dogtail-wrapper.sh /bin/dogtail-wrapper

WORKDIR /src

RUN pip3 install -r /src/requirements.txt

RUN ./install-libotrng.sh
RUN ./install-pidgin-otrng.sh

ENV PKG_CONFIG_PATH=/usr/local/lib/pkgconfig
ENV LD_LIBRARY_PATH=/usr/local/lib/

ENTRYPOINT ["/bin/dogtail-wrapper"]
CMD ["pytest"]