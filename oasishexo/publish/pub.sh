#!/bin/bash

echo "==========开始同步文件和照片=========="
sleep 3s
rsync -avP --exclude-from '/hexo/nas/config/exclude.txt' /hexo/nas/source/* /hexo/oasis/source/_posts 
find /hexo/nas/source -type d -name "photo" -exec rsync -avP {}/ /hexo/oasis/source/photo/ \;

echo "==========开始构建网站=========="
sleep 3s
cd /hexo/oasis
hexo generate

echo "==========构建网站完成=========="