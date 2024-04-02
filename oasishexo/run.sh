#!/bin/bash


cp /hexo/nas/config/_config.yml /hexo/oasis/
cp /hexo/nas/config/_config.butterfly.yml /hexo/oasis/

cd /hexo/oasis
hexo clean
hexo generate
hexo server &

. /hexo/pip/bin/activate
cd /hexo/publish
python3 app.py