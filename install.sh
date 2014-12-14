#!/bin/bash

cp ./repos/*.repo /etc/yum.repos.d/
yum install epel-release

#cache rpms
sed -i "s/keepcache=0/keepcache=1/g" /etc/yum.conf 

lastrpm=`ls -t | grep adfi | head -1`

yum localinstall ./${lastrpm}

/etc/init.d/iptables stop



