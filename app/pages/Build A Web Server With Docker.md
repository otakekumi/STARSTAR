title: Build A Web Server With Docker
date: 2017-07-18 20:34:03
tags: ['服务器相关']



最近用Docker搭了个apache服务器，放了一道题上去，理下流程。

先是找好镜像，我下载的是Ubuntu的官方镜像，ubutnu:14.04
<pre class="prettyprint">docker search ubuntu   //搜索镜像</pre>
然后便可以看到ubuntu系列的docker镜像，我下的是ubuntu:14.04,选定镜像之后下载：
<pre class="prettyprint">docker pull ubuntu:14.04      //下载镜像</pre>
下载镜像之后就新建一个容器，注意端口映射问题：
<pre class="prettyprint">docker run -it -p 44227:80 ubuntu:14.04 /bin/bash</pre>
然后开启容器，进入容器，之后的步骤就按照正常的apache服务器搭建流程。

有几个地方需要注意：

1.创建docker容器的时候，如果想通过外网访问，记得指定IP时不要指定成127.0.0.1，因为127.0.0.1是本地回环地址，外网是无法访问。

2.安装好apache之后，记得安装php环境，我就是忘了安装php环境还懵逼了一会儿

3安装完毕之后记得service apache2 start

&nbsp;

docker容器创建使用-p参数指定映射端口时，便会将该端口纳入iptables，使之对外开放