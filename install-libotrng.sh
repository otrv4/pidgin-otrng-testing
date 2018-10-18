#!/bin/bash

set -xe

rm -rf /tmp/goldilocks /tmp/libotr-ng

git clone --depth=1 https://github.com/otrv4/libgoldilocks.git /tmp/goldilocks
git clone --depth=1 https://github.com/otrv4/libotr-ng.git /tmp/libotr-ng

cd /tmp/goldilocks
autoreconf --install
./configure
make && make install

cd /tmp/libotr-ng
autoreconf --install
./configure
make && make install


