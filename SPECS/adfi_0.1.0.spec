Summary:   adfi package
Name:      adfi 
Version:   0.1.0
Release:   1
License:   GPL
Group:     System
Requires:  python,python-setuptools,mysql,mysql-devel,mysql-server,java-1.7.0-openjdk,freeradius,freeradius-mysql,freeradius-utils,nginx,curl
SOURCE0:   portal.tar.gz
SOURCE1:   nginxconf.tar.gz
SOURCE2:   www.tar.gz
SOURCE3:   aaa.tar.gz
SOURCE4:   smsadapter.tar.gz
SOURCE5:   protocal.tar.gz
SOURCE6:   supervisorconf.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Url:       http://www.adfi.cn/
Packager:  ShaoJunWu 
Prefix:    %{_prefix}
Prefix:    %{_sysconfdir}
%define    userpath /usr/share/adfi
%define	   userpath_ex \\/usr\\/share\\/adfi

%description
adfi package


%prep
%setup -c
%install
install -d $RPM_BUILD_ROOT%{userpath}
#copy web app
%{__install} -p %{SOURCE0} $RPM_BUILD_ROOT%{userpath}
tar -xf %{SOURCE0} -C $RPM_BUILD_ROOT%{userpath}
tar -xf %{SOURCE1} -C $RPM_BUILD_ROOT%{userpath}
tar -xf %{SOURCE2} -C $RPM_BUILD_ROOT%{userpath}
tar -xf %{SOURCE3} -C $RPM_BUILD_ROOT%{userpath}
tar -xf %{SOURCE4} -C $RPM_BUILD_ROOT%{userpath}
tar -xf %{SOURCE5} -C $RPM_BUILD_ROOT%{userpath}
tar -xf %{SOURCE6} -C $RPM_BUILD_ROOT%{userpath}

%post
#config mysql
echo "config mysql"
chkconfig --levels 35 mysqld on
service mysqld start
mysqladmin -u root password 123qwe
chkconfig --levels 35 mysql on
echo "create database radius;" | mysql -uroot -p123qwe

#config apps
echo "config app"
#ln -s %{userpath}/bin/adfid /etc/init.d/
#chkconfig --levels 35 adfid on
#service adfid start
#mkdir %{userpath}/logs
#echo "wait for java app start!"
#sleep 10
jarfile=`ls %{userpath}/aaa/adfi*.jar|head -1`;ln -s ${jarfile} %{userpath}/aaa/aaa.jar

#config nginx
echo "config nginx"
ln -s %{userpath}/nginxconf/adfi.conf /etc/nginx/conf.d/ 
chkconfig --levels 35 nginx on
service nginx start

#config radius
echo "config radius"
sed -i 's/^.*login.*=.*$/         login = root/g' /etc/raddb/sql.conf
sed -i 's/^.*password.*=.*$/         password = 123qwe/g' /etc/raddb/sql.conf
sed -i 's/^.*readclients.*=.*$/         readclients = yes/g' /etc/raddb/sql.conf
sed -i 's/^.*\$INCLUDE.*sql.conf.*$/        \$INCLUDE sql.conf/g' /etc/raddb/radiusd.conf
sed -i 's/^.*\$INCLUDE.*sql\/mysql\/counter\.conf.*$/        \$INCLUDE sql\/mysql\/counter.conf/g' /etc/raddb/radiusd.conf
sed -i 's/^.*\$INCLUDE.*clients.conf.*$/#\$INCLUDE clients.conf/g' /etc/raddb/radiusd.conf
sed -i 's/^#.*sql$/\tsql/g' /etc/raddb/sites-enabled/default

mysql -uroot -p123qwe -Dradius < /etc/raddb/sql/mysql/nas.sql
mysql -uroot -p123qwe -Dradius < /etc/raddb/sql/mysql/schema.sql
mysql -uroot -p123qwe -Dradius < /etc/raddb/sql/mysql/wimax.sql
chkconfig --levels 35 radiusd on
service radiusd start


#install supervisor
easy_install supervisor
echo_supervisord_conf > /etc/supervisord.conf
sed -i "s/^;\[inet_http_server\]\(.*\)$/\[inet_http_server\]\\1/g" /etc/supervisord.conf
sed -i "s/^.*port=127.0.0.1:9001\(.*\)/port=0.0.0.0:9800\\1/g" /etc/supervisord.conf
sed -i "s/^;\[include\]\(.*\)/\[include\]\\1/g" /etc/supervisord.conf
sed -i "s/^;files.*$/files = %{userpath_ex}\/supervisorconf\/\*\.conf/g" /etc/supervisord.conf


#chown -R tomcat %{userpath}/iOPAPPS/RadiusWeb
#ln -s %{userpath}/iOPAPPS/RadiusWeb/ %{tomcatapppath}
#mysql -uroot -p123qwe < %{tomcatapppath}RadiusWeb/backup/remote/mysql/radius.sql
#mysql -uroot -p123qwe < %{tomcatapppath}RadiusWeb/backup/remote/mysql/dbradius.sql 
#mysql -uroot -p123qwe < %{tomcatapppath}RadiusWeb/backup/remote/mysql/dbradius_data.sql 
#sed -i 's/c:\\\\/\/var\/log\/tomcat6\//g' %{tomcatapppath}RadiusWeb/WEB-INF/classes/log4j.properties
#sed -i 's/C:\\\\/\/var\/log\/tomcat6\//g' %{tomcatapppath}RadiusWeb/WEB-INF/classes/log4j.properties

#ldconfig
#sed -i 's/^prefix.*=.*$/prefix = %{userpath_ex}\/auteradius/g' %{userpath}/auteradius/etc/raddb/radiusd.conf 
#sed -i "s/^.*server.*=.*$/         server = \"127.0.0.1\"/g" %{userpath}/auteradius/etc/raddb/sql.conf
#sed -i 's/^\$INCLUDE.*dictionary/\$INCLUDE %{userpath_ex}\/auteradius\/share\/freeradius\/dictionary/g' %{userpath}/auteradius/etc/raddb/dictionary
#sed -i 's/^prefix=.*$/prefix=%{userpath_ex}\/auteradius/g' %{userpath}/auteradius/sbin/rc.radiusd
#sed -i 's/^rundir=.*$/rundir=\${localstatedir}\/run\/freeradius/g' %{userpath}/auteradius/sbin/rc.radiusd
#sed -i 's/\/radius.pid/\/freeradius.pid/g' %{userpath}/auteradius/sbin/rc.radiusd
#sed -i 's/^ARGS.*$/ARGS=\" -d %{userpath_ex}\/auteradius\/etc\/raddb\"/g' %{userpath}/auteradius/sbin/rc.radiusd

#ln -s %{userpath}/auteradius/sbin/rc.radiusd /etc/init.d/radiusd
#chkconfig --levels 35 radiusd on
#service radiusd start



%clean
rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_DIR/%{name}-%{version}

%postun
rm -rf %{userpath}

%files
%defattr(-,root,root)
%{userpath}
