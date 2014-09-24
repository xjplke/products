#!/bin/bash


export GOPATH="/root/goprg"
export JAVA_HOME="/usr/java/default/"

APPROOT=`pwd`
echo "APPROOT="$APPROOT

dirs='BUILD BUILDROOT RPMS SOURCES SRPMS'


if [ "$1" == "clean" ]; then
	for dir in $dirs
	do
		rm -rf $dir
	done	
	exit 0
fi

if [ "$#" == "0" ] || [ "$1" == "build" ] ;then


for dir in $dirs
do
	[ -d $dir ] || mkdir $dir 
done


go get -u github.com/xjplke/syler
go get -u github.com/xjplke/ifdaa
go get -u github.com/xjplke/smsadapter

apps="aaa www portal smsadapter"


for app in $apps
do
	[ -d ${APPROOT}/SOURCES/${app} ] || mkdir ${APPROOT}/SOURCES/${app}
	rm -rf ${APPROOT}/SOURCES/${app}/*
done

echo "build ifdaa"
AAA_PATH=${GOPATH}/src/github.com/xjplke/ifdaa
cd ${AAA_PATH}
rm -rf ${AAA_PATH}/build/libs/* 
./gradlew build
cp ${AAA_PATH}/build/libs/*.jar ${APPROOT}/SOURCES/aaa 
cp -r ${AAA_PATH}/src/main/webapp/* ${APPROOT}/SOURCES/www


echo "build syler"
SYLER_PATH=${GOPATH}/src/github.com/xjplke/syler
cd ${SYLER_PATH}
go build
cp syler ${APPROOT}/SOURCES/portal/ 

echo "build smsadapter"
SMS_PATH=${GOPATH}/src/github.com/xjplke/smsadapter
cd ${SMS_PATH}
go build
cp smsadapter ${APPROOT}/SOURCES/smsadapter/ 
cp smsadapter.conf ${APPROOT}/SOURCES/smsadapter/



fi


if [ "$#" == "0" ] || [ "$1" == "rpm" ];then

cd ${APPROOT}/SOURCES/
for dir in `ls`
do
	echo tar ${dir}
	tar -cjf ${dir}.tar.gz ${dir}
done

fi





