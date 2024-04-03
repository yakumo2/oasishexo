# oasishexo

1. 封装了hexo
2. 封装了一个发布hexo（基于flask）

- `oasishexo`: 直接用来build镜像
- `nas`: 包含一些config文件需要挂在到镜像上


## 文件结构
```
-- oasishexo # 镜像目录
    L run.sh # 镜像启动时的entrypoint，负责启动hexo和发布服务
    L dockerfile # docker制作文件
    L publish # 基于Flask的发布服务
        L app.py    # 主程序
        L hello.sh  # 测试脚本
        L pub.sh    # 简单发布脚本，不清除现有
        L cleanpub.sh   # 删除发布脚本，清除现有
        L templates     
            L index.html    #发布服务的入口页面

-- nas # 非docker内部，放在本地挂载给容器
    L config
        L exclude.txt # 把博客的markdown从本地的source目录向hexo的source目录同步的过程中需要忽略的文件，例如一些untitle、css等等
        L _config.yml # hexo的主配置文件，这里默认定义了使用butterfly主题
        L _config.butterfly.yml # butterfly的配置文件，做了一些自定义修改
```

## docker相关

### 打包

```
# 制作amd64的版本，适合x86架构
$ docker buildx build --platform linux/amd64 oasishexo --load -t oasishexo:alpine-amd64

# 制作arm64的版本，适合M芯片的mac
$ docker buildx build --platform linux/arm64 oasishexo --load -t oasishexo:alpine-arm64
```

### 导出镜像

```
# 导出amd64版本
$ docker save -o oasishexo-alpine-amd64.tar oasishexo:alpine-amd64

# 导出arm64版本
$ docker save -o oasishexo-alpine-arm64.tar oasishexo:alpine-arm64
```

### 启动容器
```
docker run -it -d -p 4000:4000 -p 4001:5000 -v <local config>:/hexo/nas  -v <local source>:/hexo/nas/source --name hexo oasishexo:alpine-arm64
```

- 开放端口`4000`:`4000`: hexo服务端口
- 开放端口`4001`:`5000`: 发布服务端口
- 挂载`<local config>`:`/hexo/nas`: 主要是配置文件
- 挂载`<local source>`:`/hexo/nas/source`: 需要发布的markdown源文件

## 使用

1. 按照上面的说明开放好端口，挂载好目录
2. 启动容器，等容器启动完成，下面两个页面就可以访问了
    1. 博客：`http://localhost:4000` (默认页面)
    2. 发布系统: `http://localhost:4001` (发布页面）
3. 第一次启动的时候，进入发布系统，进行一次`清除发布`，会清除掉默认的内容，换成`本地source`里的内容
4. 打开博客就OK了
5. 后续重启容器就正常了，不需要专门`清除发布`了

