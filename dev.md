# 目录

不知道md怎么插入hhh

# 文件结构说明

## source

是存储大的二进制文件的地方

二级目录是应用名

## config

是存储配置文件的位置

二级目录是应用名，内部配置文件分别对应相应的系统

- win.yml
- linux.yml
- mac.yml

以qq为例：

```yml
qqnt: &qqnt # 这里添加引用，便于default使用
  desc: qqNT版本 # 描述
  compatible: # 兼容的系统，通常为大版本号或者发行版
    - Debian
  installation_page: # 官网安装说明地址
    - xxxx
  comment: # 包含说明的安装过程
    - \# 说明
    - xxxx
  args: # （opt）run的运行参数
    - xxxx
  run:  # （opt）默认运行
    - xxxx
  config: # (opt) 配置文件的位置，用于备份
    - xxxx
default: # 默认配置，如果没有特殊的配置，就使用这个
  *qqnt # 引用
```

## doc

这个文件夹用来记录安装过程的一些描述，这样可以把一些软件的安装过程详细的描述出来，尽可能的丰富一个软件的安装问题，避免上互联网上到处寻找

未来可能会派生版本，不过最好一个文件解决

# ENV

一些环境变量，以及一些预定义的变量

- software_dir 所有软件的装目录
- platform 架构x86, arm等
- download_dir 默认的下载目录

# API

避免重复早轮子的一些小工具

## github-latest-download

获取github上最新的release版本

```bash
bash utils/github-latest-download.sh user/repo pattern file_name
```