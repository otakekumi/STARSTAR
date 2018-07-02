title: Docker Notes
date: 2017-07-06 23:39:55
tags: ['服务器相关']


## 基础内容
Docker是一个开源的引擎，可以为应用创建一个容器。
Docker常用于：
1. web应用的自动化打包和发布
2. 自动化测试和持续集成，发布
3. 在服务型环境中部署和调整数据库或其他后台应用
4. 从头编译或者扩展现有的openshift或cloud founary平台来搭建自己的PaaS环境

什么是容器技术：
容器有效的将单个操作系统管理资源划分到孤立的组中，以更好的在孤立的组中平衡有冲突的资源使用需求。与虚拟化相比，这样既不需要指令级模拟，也不需要即时编译。容器可以再核心CPU本地运行指令，而不需要任何专门的解释机制。此外，也避免了准虚拟化（paravirtualization）和系统调用替换中的复杂性。

Docker系统有两个程序：docker服务端和docker客户端。其中docker服务端是一个服务进程，管理所有的容器。docker客户端则类似于docker服务端的远程控制器，可以用来控制docker的服务端进程。大部分情况下，docker的服务端和客户端运行于同一台机器上。

docker客户端：
实际上就是docker的二进制程序，是主要的用户与docker交互方式。它接受用户指令并与背后的docker服务端通信，如此来回


docker三个部件：

1. Docker镜像    Docker images
2. Docker仓库    Docker registeris
3. Docekr容器    Docker containers

Docker镜像类似于虚拟机镜像，可以将其理解为一个只读的模板。一个镜像可以包含一个基本的操作系统环境。

Docker镜像是创建Docker容器的基础。通过版本管理和增量的文件系统，Docker提供了一套非常简单的机制来更新和创建现有的镜像。
Docker镜像由若干层组成，当使用docker pull命令下载时会获取并输出镜像的各层信息。当不同的镜像包括相同的层时，本地仅存储层的一层内容，减小了需要的存储空间。

Docker容器类似于一个轻量级的沙箱，Docker利用容器来运行和隔离应用。容器是从镜像创建的应用运行实例。

可以将容器看做一个简易版的Linux系统环境（包括root用户权限，进程空间，用户空间和网络空间等）以及运行在其中的应用程序打包而成的盒子。

Docker仓库类似于代码仓库，它是Docker集中存放镜像文件的场所。

镜像是运行容器的前提，可以使用docker pull 命令从docker hub中下载镜像。

通常情况下，描述一个镜像需要包括“名称+标签”信息，对于Docker镜像来说，如果不显式指定TAG，则默认会选择latest标签，这会下载仓库中最新版本的镜像。

下载过程中可以看出，镜像文件一般由若干层（layer）组成，hash值是层的唯一id。使用docker pull命令下载时会获取并输出镜像的各层信息。当不同的镜像包括相同的层时，本地仅存储层的一份内容，减小了需要存储的空间。

查看镜像信息：docker images
在列出的信息中，可以看到以下几个字段的信息：

1.  来自哪个仓库
2.  镜像的标签信息，如14.04
3.  镜像的ID
4.  创建时间
5.  镜像大小

镜像的ID是镜像的唯一标识。

标签（TAG）信息用来标记来自同一个仓库的不同镜像。例如ubuntu仓库中有多个镜像，通过TAG信息来区分发行版本，包括10.04，,1.04等。

镜像大小信息只是表示镜像的逻辑体积大小，实际上由于相同的镜像层本地只会储存一份，物理上占用的存储空间会小于各镜像的的逻辑体积之和。

容器是Docker的另一个核心概念。
简单来说，容器是镜像运行的一个实例。所不同的是，镜像是静态的只读文件，而容器带有运行时需要的可写文件层。

如果将虚拟机看成是模拟运行的一整套操作系统（包括内核，应用运行环境和其他系统环境）和跑在上面的应用，那么Docker容器就是独立运行的一个（或一组）应用，以及他们必需的运行环境。


## 创建容器
** **
### 1.创建容器     
docker create IMAGE:TAG

示例：docker create -it ubuntu:14.04

 操作完成后，会生成一个处于停止状态的docker，可以使用start命令来启动这个docker，如果想要查看所有的容器的话，可以使用docker ps -a,假设create操作生成的容器ID为：20adf2abf2e5d145688c386df46f7d0ba70aa5d5faa3cd96a52dcdc0b6142

## 2.启动容器     
docker start ID
示例：docker start  20a
ID即为容器的ID，这是容器的唯一标识，在进行start操作时，并不用将ID全写出，只要可让docker判断出是哪个容器即可。


## 3.新建并启动容器      
docker run IMAGE:TAG FILE

示例：docker run ubuntu:14.04 /bin/echo "hello world"
run操作等价于先create，后start。

可以使用如下的明洞启动一个bash终端：docker run ubuntu /bin/bash

除了终端这种交互式的容器，还可以创建长期运行的容器。守护式容器没有交互式会话，适合运行应用程序和服务。大多数时候需要以守护式来运行容器。
可以通过加参数  -d 实现，如： docker run -d ubuntu xxxxxx

##4.终止容器 
docker stop [-t|--time[=10]] [CONTAINER... ]


## 5.进入容器
使用-d参数，容器以守护态运行，在容器启动后会自动进入后台，用户无法看到容器中的信息，也无法进行操作。

此时若想进入容器进行操作，可以使用attach或exec命令，以及第三方的nsenter工具等。

### 5.1 attach命令

attach命令是docker自带命令,命令格式为：
docker attach [--datach-keys[=[]]] [--no-stdin] [--sig-proxy[=true]] CONTAINER
实际使用如下，先run一个容器：

 >   docker run -itd ubuntu   
 >   docker ps -a   
 >   docker attach

该方法的缺陷在于若多个窗口使用attch命令连接到容器，所有窗口会同步显示，当某个窗口因命令阻塞时，其他窗口也无法执行操作。
### 5.2exec命令
Docker自从1.3.0版本起提供了一个更加方便的exec命令，可以直接在容器内执行任意命令。

 >   docker exec [-d|--detach]    
 >   [--detach-keys[=[]]]    
 >   [-i|--interactive]   
 >   [--privileged]   
 >   [-t|--tty]   
 >   [-u|--user=[user]]
 >   CONTAINER COMMAND [ARG...]


 > -i | --interactive = true|false 打开标准输入接受用户输入命令   
 > --privileged = true|false        是否给执行命令以高权限，默认为false   
 >   -t | --tty = true|false            分配为终端，默认fasle   
 >   -u | --user = ""                    执行命令的用户名或ID   

 > docker exec -it 243c /bin/bash

