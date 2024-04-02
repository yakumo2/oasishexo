#!/bin/bash

echo "==========开始删除原source/_posts=========="
sleep 3s
rm -rf /hexo/oasis/source/_posts/*
rm -rf /hexo/oasis/source/photo/*

echo "==========删除完成=========="

echo "==========拷贝主配置文件=========="
sleep 1s
cp /hexo/nas/config/_config.yml /hexo/oasis/

echo "==========拷贝butterfly配置文件=========="
sleep 1s
cp /hexo/nas/config/_config.butterfly.yml /hexo/oasis/

echo "==========开始同步md文件和图片文件:=========="

sleep 3s
rsync -avP --exclude-from '/hexo/nas/config/exclude.txt' /hexo/nas/source/* /hexo/oasis/source/_posts 
find /hexo/nas/source -type d -name "photo" -exec rsync -avP {}/ /hexo/oasis/source/photo/ \;
echo "==========同步完成=========="

echo "==========开始构建网站:=========="
cd /hexo/oasis
hexo clean
hexo generate

echo "==========构建完成=========="