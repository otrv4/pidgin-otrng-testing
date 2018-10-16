FROM ubuntu:trusty


RUN apt-get update && apt-get upgrade -y -o Dpkg::Options::="--force-confold"
RUN apt-get install -y software-properties-common
RUN apt-add-repository ppa:ubuntu-mate-dev/trusty-mate
RUN apt-get update

# Minimum Gnome environment
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install \
  --no-install-recommends xvfb ubuntu-mate-core ubuntu-mate-desktop

# Required for TCNode in dogtail
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install \
    python-dev python-imaging\
    libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev \
    liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev

# Python env for dogtail
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install \
   --no-install-recommends python python3-pip python-gobject

# Pidgin
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install \
    pidgin

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

VOLUME /src
VOLUME /tmp/dogtail-root

ADD dogtail-wrapper.sh /bin/dogtail-wrapper
ADD . /src

WORKDIR /src
RUN pip3 install -r /src/requirements.txt

ENTRYPOINT ["/bin/dogtail-wrapper"]
CMD ["pytest"]