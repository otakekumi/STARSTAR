title: CVE-2017-5487:Content Injection Vulnerability in WordPress 4.7 and 4.7.1
date: 2017-04-09 00:49:47
tags: ['PHP安全相关']


最近在漏洞盒子上提交了两个wordpress的REST API的越权漏洞，现在做一下学习总结

1.


REST全称是REpresentational State Transfer，即表述性状态转移.

换个角度看，REST API首先是个API，它与普通API不同的地方在于它是可以通过URL来完成操作的，这样就极大地方便了前端，但同时问题就出来了，如果任意访问者都可使用REST API则会形成越权漏洞，在Wordpress的这个漏洞中不需要任何权限，只是通过简单的更改URL和Content-Type就可以实现更改页面内容

2.

在知道了这个漏洞的成因之后，我们需要知道REST API操作资源的方式，然后在包含该漏洞的网页上操作即可。

REST API通过GET,POST,PUT,DELETE,Options，Head来操作资源，并且post后面并不需要具体的路径，比如你想访问id为32的文章，一般方法是 ?id=32 ，但是post只需要32就可以了。

在有漏洞存在可能的网页上输入url:/wp-json/wp/v2/posts，如果返回的是json类数据，那么很有可能存在漏洞，如图：

![](http://www.meizj.com.cn/wp-content/uploads/2017/03/Inked1_LI.jpg)

接下来就是找定id，利用api姿势来修改特定内容，这里不做过多说明(っ´Ι`)っ

3.分析

去下了份wp4.7.1，开始看REST API相关源码分析漏洞成因。

首先分析漏洞是属于权限认证失误导致越权漏洞，将目标缩小到权限检查函数，再结合目前利用最多的方式看，应该是在对数据更新这一块的权限认证产生了漏洞，打开wp有关rest pai的源码进行分析。

在漏洞利用的过程中，我们通过构造一个url来进行检验，这个步骤通过注册路由来实现，而我们在\wp-wpincludes\rest-api\endpoints\class-wp-rest-posts-controller.php开头处便发现了一个名为register_routes的功能，再往下看找到更新数据的register_rest_route，发现有个正则表达式生成，这里经过看其他大大的测试以及自己的复现，发现$_GET和$_POST的优先级确实高于正则生成的优先级，所以可以直接将这个正则忽略掉，往下看，里面调用了update_item以及update_item_permissions_check两个函数。![](http://www.meizj.com.cn/wp-content/uploads/2017/04/1.png)

猜测逻辑为，先进行权限检查再进行数据更新，若权限检查失败，则不进行数据更新，也就是说，漏洞的源头在update_item_permissions_check中。

在该文件中查找这两个函数。

![](http://www.meizj.com.cn/wp-content/uploads/2017/04/2-1.png)

大概阅读一下，该函数由四个if以及开头两个函数组成，若想达成权限绕过的目的，突破口便在第一个if的$post上，使get_inistance($post)返回false即可达到绕过的目的，跟进get_post函数，

![](http://www.meizj.com.cn/wp-content/uploads/2017/04/3-1.png)

首先$post不为空，过第一个if，$post不是WP_POST的对象，过第二个，进第三个，先不忙着跟进get_inistance方法，继续向下阅读，$_post不为空，过第四个，接下来就是的几个函数都很简单，最后就是返回$_post ,现在跟进get_inistance方法，

![](http://www.meizj.com.cn/wp-content/uploads/2017/04/4.png)

第一个if语句判断$post_id是不是整数，如果不是，则返回false，划重点！！这里就可以返回false了！！也就是说我们只要使$post_id不为整数即可绕过权限检查。

绕过权限检查之后，会进入update_item函数，

![](http://www.meizj.com.cn/wp-content/uploads/2017/04/5.png)

可以看到开头就是一个int类型转换，再联系到php的弱类型转换,123qwe经过转换就是123，也就是是说，请求id为123qwe时，绕过权限检查，并且能对id为123的文章进行操作。

至此漏洞分析结束。

因为这个分析主要是复现学习作用，所以参考了蛮多其他大牛的分析过程，所以大体思路会有些眼熟，就这样了，睡觉。

<del>（注意这个洞是部分4.7.1和4.7.0含有的，想复现的小伙伴啊。。。。。</del>