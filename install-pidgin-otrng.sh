#!/bin/bash

set -xe


rm -rf /tmp/pidgin-otrng /src/base_purple/plugins/*

git clone --depth=1 https://github.com/otrv4/pidgin-otrng.git /tmp/pidgin-otrng
cd /tmp/pidgin-otrng
./autogen.sh
./configure
make && make install
cp /usr/local/lib/pidgin/* /src/base_purple/plugins


