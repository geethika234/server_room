mkdir /path/of/folder/"$(date +"%Y-%m-%d")"
find /path/of/folder -mindepth 1 -maxdepth 1 -type d -ctime +6 | xargs rm -rf
