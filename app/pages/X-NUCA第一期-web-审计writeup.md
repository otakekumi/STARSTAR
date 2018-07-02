title: X-NUCA第一期 web 审计writeup
date: 2017-03-02
tags: ['WriteUp']


x-nuca第一期已经打完差不多一个月了，但是在网上翻了一圈，发现.git审计这个题目的wp貌似还没有看到，再加上现在在等车，于是想着不如干脆把wp放出来。因为时间过去了蛮久，所以有些地方的回忆会有些偏差，还请不要在意，欢迎交流，qq:960596293

首先根据提示是.git泄漏，这个不用多说，把源码拿了下来，这里我就不放图了，然后就是先看看整个的大体结构，通读一遍流程，然后会发现一个非常奇怪的文件-common.php，这里面的foreach是个变量覆盖的漏洞，应该是dedecms的变量覆盖拿过来的
```php
foreach (array('_COOKIE','_POST','_GET') as $_request)  
{
    foreach ($$_request as $_key=&gt;$_value)  
    {
        $$_key=  $_value;
    }
}
```
这个漏洞的触发方法就是，假如此时传入get参数_SESSION["name"]=123，那么_SESSION与$就会拼接在一起，形成$_SESSION["name"]=123，当然这个方法是不行的，因为common.php里面有个坑了我很久地方就是他把session_start()放在了后面，这样我们前面注册的session就会被销毁。但是基本可以确定，这个漏洞是有用的。

继续阅读代码，着重观察flag出现的地方，然后会在以下几个文件中发现在某些条件下输出flag：

do-changepass.php     user.php

$do-changepass.php输出flag的关键在于使$userinfo["id"] == 1，并且$userinfo继承自session，因此这里的就需要覆盖session，user.php输出flag的关键在于$userinfo["username"] == admin，一开始想的是能不能通过注入来搞事，然后发现全用的PDO，于是放弃注入，转向变量覆盖。在覆盖的过程中，有几个地方需要注意：
```php

include_once("common.php");
$dbh = new PDO(DSN, DB_USER, DB_PASSWD);
$sql = "select * from user where username = :username";
$sth = $dbh->prepare($sql);
$sth->execute(array(':username'=>$username));
$res = $sth->fetch(PDO::FETCH_ASSOC);
if($res !== false) {
    header("Location: error.php?msg=username%20has%20been%20used!");
    die();
}
$sql = "insert into user (username, password, role) values(:username, :password, 1)";
$sth = $dbh->prepare($sql);
$res = $sth->execute(array(':username'=>$username, ':password'=>$password));
if($res === false) {
    header("Location: error.php?msg=register%20error!");
    die();
}

$sql = "select * from user where username = :username and password = :password";
$sth = $dbh->prepare($sql);
$sth->execute(array(':username'=>$username, ':password' => $password));
$res = $sth->fetch(PDO::FETCH_ASSOC);
if($res === false) {
    header("Location: error.php?msg=register%20error!");
    die();
}
$userinfo["id"] = $res["id"];
$userinfo["username"] = $username;
$userinfo["password"] = $password;
$_SESSION["userinfo"] = $userinfo;
$userinfo["role"] = $res["role"];
header("Location: index.php");

```

可以看到它在给session赋值时，是使用的$userinfo，这里就是突破口，php是弱类型语言，假如传进userinfo=1，此时$_SESSION["userinfo"]的值便是1，而在do_changepass.php中，有一个$userinfo["id"]的判断，因为此时的userinfo是继承自session的，所以再结合php的弱类型，$userinfo["id"] 这个不存在的键便会被解析成 $userinfo[0]，再被解析成1，所以即可通过判断，拿到flag。

ps:在写到一半的时候，发现原来有师傅已经写了，尴尬....但是都写了一半了，还是继续写完放出来吧