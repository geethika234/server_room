cp -b /path/of/folder/image.jpg /path/of/folder/"$(date +"%Y-%m-%d")"

cd /path/of/folder/"$(date +"%Y-%m-%d")"
mv image.jpg  "$(date +"%X")".jpg
