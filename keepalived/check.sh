!#/bin/bash

res=$(cat /etc/keepalived/res)

if [ $res != 1 ]
then
    systemctl stop keepalived
fi
