#!/bin/bash

cp ./repos/*.repo /etc/yum.repos.d/
#yum install epel-release

#cache rpms
sed -i "s/keepcache=0/keepcache=1/g" /etc/yum.conf 

lastrpm=`ls -t | grep adfi | head -1`

yum localinstall ./${lastrpm}



echo "#!/bin/bash
supervisord -c /etc/supervisord.conf
/etc/init.d/iptables stop
" > /etc/rc.d/init.d/adfid.sh
rm -rf /etc/rc.d/init.d/z99adfid.sh
ln -s /etc/rc.d/init.d/adfid.sh /etc/rc.d/rc2.d/S99adfid.sh
ln -s /etc/rc.d/init.d/adfid.sh /etc/rc.d/rc3.d/S99adfid.sh
ln -s /etc/rc.d/init.d/adfid.sh /etc/rc.d/rc4.d/S99adfid.sh
ln -s /etc/rc.d/init.d/adfid.sh /etc/rc.d/rc5.d/S99adfid.sh
chmod 755 /etc/rc.d/init.d/adfid.sh

/etc/rc.d/init.d/adfid.sh

