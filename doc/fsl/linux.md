# 注意事项

fsl的直接安装方法会导致conda被替换成fslconda，之后用conda安装的软件会出现问题，此时修改配置文件或者添加channel需要通过`conda info`找到配置文件例如默认的`/usr/local/fsl/.condarc`，然后修改该文件即可

