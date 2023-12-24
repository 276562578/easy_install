#!/bin/bash

repos=$1
#repos=rustdesk/rustdesk
url_releases="https://api.github.com/repos/$repos/releases/latest"
pattern=$2
#pattern=x86_64.deb
file_name=$3
#file_name=rustdesk.deb
url_download=$(curl -sL $url_releases | grep '"browser_download_url":' | sed -E 's/.*"([^"]+)".*/\1/' | grep $pattern)
wget $url_download -O /tmp/$(echo $repos | awk -F '/' '{print $2}')
