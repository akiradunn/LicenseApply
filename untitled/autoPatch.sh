#! /bin/bash
##this script is used to install new front module conveniently!!!
cd /site/project/appfront/
echo "------start to unzip appfront.zip file"
unzip appfront.zip
if [ $? -ne 0 ]; then
    echo "can't find appfront.zip"
else
    echo "------finish unzip operation!"
    mv appfront.zip ../
    cd ../untitled/
    rm -rf appfront/
    cd ../
    echo "---start move appfront---"
    mv appfront/ untitled/
    cd /usr/local/nginx/sbin/
    echo "---start reload nginx---"
    ./nginx -s reload
    cd /site/project/untitled/
    echo "---start activate virtualenv---"
    source /site/project/untitled/centosenv/bin/activate
    uwsgiPid=`netstat -anp | grep 8888 | awk '{printf$7}' | cut -d / -f1`
    echo "-------uwsgiPid is $uwsgiPid"
    if [ -z $uwsgiPid ]; then 
	uwsgi --ini uwsgi.ini
    else
	kill -s 9 $uwsgiPid
	echo "---start uwsgi server---"
	uwsgi --ini uwsgi.ini
    fi
fi
