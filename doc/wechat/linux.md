# 安装方式

linux微信目前官方版进度缓慢，所以派生出了多种安装方式

1. ~~electron+web登陆，这种方式已死~~
2. 官方版本过于老旧，且性能很差（[点此跳转](https://www.ubuntukylin.com/applications/106-cn.html)）
3. 国产系统集成的版本（目前没途径搞到）
4. 基于deepin-wine的版本（暂时推荐，[点此跳转](https://github.com/vufa/deepin-wine-wechat-arch)但这个库是基于AUR的）
5. 根据4进行的docker打包（推荐）
6. 盒装微信（有一些小bug，[点此跳转](https://github.com/huan/docker-wechat)）
7. spark版本的com.qq.weixin.spark（当前最佳）

# 使用方法

新建一个目录之后复制docker-compose.yml文件到该目录下，然后根据描述修改相应的变量，运行`docker-compose up -d`即可

为了更方便之后使用，可以添加 /usr/share/applications/wechat.desktop 文件来新建快捷方式

```desktop
#!/usr/bin/env xdg-open
[Desktop Entry]
Encoding=UTF-8
Type=Application
Categories=chat;Network;
# 图标可以在 https://cdn.lwqwq.com/dl/wechat.svg 这里下载
Icon=//wechat.svg
Name=WeChat
Name[zh_CN]=微信
Comment=Tencent WeChat Client on Deepin Wine
StartupWMClass=WeChat.exe
Exec=docker exec wechat /opt/apps/com.qq.weixin.spark/files/run.sh
```

有问题可以进入docker内部进行调试`docker exec wechat /opt/apps/com.qq.weixin.spark/files/run.sh`

# spark版本（推荐）

这个版本功能最多，但我打包的docker镜像有一些权限问题没有配置好

## 安装过程

## Dockerfile

```Dockerfile
FROM archlinux
# 配置软件
# 这个spark的aur包缺字体，我一直不会自动安装optDepend部分，所以就手动安装了
RUN echo -e '[multilib]\nInclude = /etc/pacman.d/mirrorlist\n[archlinuxcn]\nServer = https://mirrors.ustc.edu.cn/archlinuxcn/$arch' >>/etc/pacman.conf && \
    echo -e 'Server = https://mirrors.ustc.edu.cn/archlinux/$repo/os/$arch\nServer = https://geo.mirror.pkgbuild.com/$repo/os/$arch\nServer = https://mirror.rackspace.com/archlinux/$repo/os/$arch\nServer = https://mirror.leaseweb.net/archlinux/$repo/os/$arch' >/etc/pacman.d/mirrorlist && \
    pacman -Sy --noconfirm git wget binutils fakeroot go make gcc autoconf base-devel sudo archlinuxcn-keyring xdotool xorg-xinit xorg-twm xorg-xclock xterm xorg xorg-server-xvfb dbus-python wqy-microhei&& \
     echo "DEEPIN_WINE_SCALE=1.25" >> /etc/environment

#  新建用户
RUN useradd -m builder && \
    echo "builder ALL=(ALL) NOPASSWD: ALL">>/etc/sudoers
    
# 构建yay
USER builder
RUN cd ~/ && git clone https://aur.archlinux.org/yay.git && \
    go env -w GO111MODULE=on && \
    go env -w GOPROXY=https://goproxy.cn,direct && \
    export GO111MODULE=on && \
    export GOPROXY=https://goproxy.cn && \
    cd ~/yay && makepkg -si --noconfirm
# 用yay安装com.qq.weixin.spark这个aur包，同时修改wine为wine-for-wechat以解决透明框框问题
# 但是这个包的lilac大佬的key倒入有问题，所以通过重建的方式修复（这一步卡了好久）
RUN mkdir -p ~/.cache/yay && cd ~/.cache/yay && yes | yay -G com.qq.weixin.spark && \
    cd com.qq.weixin.spark && \
    sed -i "s/'wine'/'wine-for-wechat'/g" PKGBUILD  && \
    sed -i 's/"wine"/"wine-for-wechat"/g' PKGBUILD && \
    cd ~ && yes|yay -S com.qq.weixin.spark && \
    sudo pacman-key --init && \
    sudo pacman-key --populate archlinux && \
    sudo pacman-key --populate archlinuxcn && \
    yes | yay -S wine-for-wechat

```

## docker-compose

挂载目录之后镜像内部会变为root权限导致无法运行，我修改了uid也不行，所以只好在镜像内部以root来运行了，希望有大佬可以完善这一部分

```yml
version: '3'

services:
  wechat:
    image: wechat
    container_name: wechat
    ipc: host
    # 为了使用音频设备
    privileged: true
    environment:
      - DISPLAY=:1
      # 我是debian，输入发是ibus的，其他可能是fcitx
      - XMODIFIERS=@im=ibus
      - GTK_IM_MODULE=ibus
      - QT_IM_MODULE=ibus
      # 音频视频设备id
      - AUDIO_GID=29
      - VIDEO_GID=44
      - GID=1000
      - UID=1000
      - TZ=Asia/Shanghai
    volumes:
    # 挂载微信缓存文件夹
      - /home//software/wechat/DoChat/WeChat Files/:/root/WeChat Files/
    # 为了方便发送截图用的
      - /home//图片/截图:/截图
      - /home//software/wechat/DoChat/Applcation Data/:/root/.wine/drive_c/users/user/Application Data/
    # x11显示
      - /tmp/.X11-unix:/tmp/.X11-unix
    # x11认证
      - $HOME/.Xauthority-docker:/root/.Xauthority-docker
      - /run/user/1000/pulse:/run/pulse
    devices:
      - /dev/snd:/dev/snd
      - /dev/video0:/dev/video0
      - /dev/video1:/dev/video1
    extra_hosts:
      - "dldir1.qq.com:127.0.0.1"
    restart: unless-stopped
    tty: true

```

# deepin-wine-arch版本（有一些小问题）

感谢[大佬的镜像](https://nyac.at/posts/deepin-wine-wechat-in-docker)帮助度过了前期的使用

折腾了一整天处理各种问题，主要是网络问题，[deepin-wine-wechat-arch](https://github.com/vufa/deepin-wine-wechat-arch)的安装方式中只有yay可行，因为有一些以来包是只有yay中有，否则的话就得自己手动编译，所以下载pkg.tar.zx文件的方式和git本地打包的方式都不能解决依赖的问题，所以选择了yay的方式

## 安装过程

注意点：

1. 打包的时候如果通过`--build-arg "HTTPS_PROXY="`的方式进行代理会从头生成id不一致的镜像
2. `--squash`可以缩小镜像文件大小，需要修改`/etc/docker/daemon.json`文件加入`"experimental": true`，同时`systemctl restart docker`才行，reload方式无效

###  镜像选择

deepin, archlinux:base, archlinux:base-devel中选择了base，尽可能的减小体积

### 更换源

加入archlinuxcn，同时替换为ustc的镜像

### 软件安装

- binutils fakeroot  
是makepkg所需要的
- go make gcc autoconf base-devel  
是yay的编译以及后续过程中需要的
- archlinuxcn-keyring  
使用archlinuxcn所需
- xdotool xorg-xinit xorg-twm xorg-xclock xterm xorg xorg-server-xvfb   
构建的自动安装微信用的工具

## Dockerfile

```Dockerfile
FROM archlinux
ENV https_proxy="socks5://172.16.193.203:7890"

# 配置软件
RUN echo -e '[multilib]\nInclude = /etc/pacman.d/mirrorlist\n[archlinuxcn]\nServer = https://mirrors.ustc.edu.cn/archlinuxcn/$arch' >>/etc/pacman.conf && \
    echo -e 'Server = https://mirrors.ustc.edu.cn/archlinux/$repo/os/$arch\nServer = https://geo.mirror.pkgbuild.com/$repo/os/$arch\nServer = https://mirror.rackspace.com/archlinux/$repo/os/$arch\nServer = https://mirror.leaseweb.net/archlinux/$repo/os/$arch' >/etc/pacman.d/mirrorlist && \
    pacman -Sy --noconfirm git wget binutils fakeroot go make gcc autoconf base-devel sudo archlinuxcn-keyring xdotool xorg-xinit xorg-twm xorg-xclock xterm xorg xorg-server-xvfb dbus-python && \
     echo "DEEPIN_WINE_SCALE=1.25" >> /etc/environment
     
#  新建用户
RUN useradd -m builder && \
    echo "builder ALL=(ALL) NOPASSWD: ALL">>/etc/sudoers
    
# 构建yay和安装wechat，分布安装解决避免失败构建缓慢
USER builder
RUN cd ~/ && git clone https://aur.archlinux.org/yay.git && \
    go env -w GO111MODULE=on && \
    go env -w GOPROXY=https://goproxy.cn,direct && \
    export GO111MODULE=on && \
    export GOPROXY=https://goproxy.cn && \
    cd ~/yay && makepkg -si --noconfirm
RUN yay -S --noconfirm lib32-udis86-git
RUN yay -S --noconfirm deepin-wine6-stable
RUN yay -S --noconfirm deepin-wine-helper
RUN yay -S --noconfirm deepin-wine-wechat

# 安装微信setup
RUN bash -c "Xvfb :9 -screen 0 1024x768x24 &" && \
    export DISPLAY=:9 && \
    bash /opt/apps/com.qq.weixin.deepin/files/run.sh && \
    sleep 40 && \
    xdotool key Tab Tab Tab Tab Tab && \
    xdotool key Return  && \
    xdotool key Tab Tab Tab Tab Tab Tab && \
    xdotool key Return && \
    sleep 10 && \
    xdotool key Tab Tab Tab && \
    xdotool key Return && \
    sleep 5 && \
    xdotool key Return
RUN yay -Scc --noconfirm && \
    rm -rf ~/yay && \
    rm ~/.cache/yay/*

# 清理环境
USER root
RUN pacman -Rsu --noconfirm git wget binutils fakeroot go make gcc autoconf base-devel xdotool xorg-xinit xorg-twm xorg-xclock xterm xorg xorg-server-xvfb yay && \
    pacman -Scc --noconfirm && \
    rm /var/cache/pacman/pkg/*

USER builder
ENV https_proxy=""

```

## docker-compose

```yml
version: '3'

services:
  wechat:
    image: wechat
    container_name: wechat
    ipc: host
    # 为了使用音频设备
    privileged: true
    environment:
      - DISPLAY=:1
      # 我是debian，输入发是ibus的，其他可能是fcitx
      - XMODIFIERS=@im=ibus
      - GTK_IM_MODULE=ibus
      - QT_IM_MODULE=ibus
      # 音频视频设备id
      - AUDIO_GID=29
      - VIDEO_GID=44
      - GID=1000
      - UID=1000
      - TZ=Asia/Shanghai
    volumes:
    # 挂载微信缓存文件夹
      - /home//software/wechat/DoChat/WeChat Files/:/home/builder/WeChat Files/
    # 为了方便发送截图用的
      - /home//图片/截图:/截图
      - /home//software/wechat/DoChat/Applcation Data/:/home/builder/.wine/drive_c/users/user/Application Data/
    # x11显示
      - /tmp/.X11-unix:/tmp/.X11-unix
    # x11认证
      - $HOME/.Xauthority-docker:/root/.Xauthority-docker
      - /run/user/1000/pulse:/run/pulse
    devices:
      - /dev/snd:/dev/snd
      - /dev/video0:/dev/video0
      - /dev/video1:/dev/video1
    extra_hosts:
      - "dldir1.qq.com:127.0.0.1"
    restart: unless-stopped
    tty: true

```

