title: MOCTF Web400 Writeup
date: 2018-02-13 21:31:56
tags: ['PHP安全相关']


打开页面就是源码,index.php:

```php
<?php
error_reporting(0);
include('config.php');
header("Content-type:text/html;charset=utf-8");
function get_rand_code($l = 6) {
    $result = '';
    while($l--) {
        $result .= chr(rand(ord('a'), ord('z')));
    }
    return $result;
}

function test_rand_code() {
    $ip=$_SERVER['REMOTE_ADDR'];
    $code=get_rand_code();
    $socket = @socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
    @socket_connect($socket, $ip, 8888);
    @socket_write($socket, $code.PHP_EOL);
    @socket_close($socket);
    die('test ok!');
}

function upload($filename, $content,$savepath) {
    $AllowedExt = array('bmp','gif','jpeg','jpg','png');
    if(!is_array($filename)) {
        $filename = explode('.', $filename);
    }
    if(!in_array(strtolower($filename[count($filename)-1]),$AllowedExt)){
        die('error ext!');
    }
    $code=get_rand_code();
    $finalname=$filename[0].'moctf'.$code.".".end($filename);
    file_put_contents("$savepath".$finalname, $content);
    usleep(3000000);
    unlink("$savepath".$finalname);
    die('upload over!');
}

$savepath="uploads/".sha1($_SERVER['REMOTE_ADDR'])."/";
if(!is_dir($savepath)){
    $oldmask = umask(0);
    mkdir($savepath, 0777);
    umask($oldmask);
}
if(isset($_GET['action']))
{
    $act=$_GET['action'];
    if($act==='upload')
    {
        $filename=$_POST['filename'];
        if(!is_array($filename)) {
            $filename = explode('.', $filename);
        }
        $content=$_POST['content'];
        waf($content);
        upload($filename,$content,$savepath);
    }
    else if($act==='test')
    {
        test_rand_code();
    }
}
else {
    highlight_file('index.php');
}
?>
```

先大概理一下流程：

1. 根据action参数判断功能
2. upload功能为上传文件
3. test为查看随机数
4. upload方法中，最终的文件名是由用户的参数拼接而成的
5. unlink删除上传的文件

上传功能的问题只要产生在end函数和count函数的差异，变量$filename[count($filename)-1]是根据下标进行取值，而end取得是数组参数的最后一位。

也就是说，在传参形如：filename[1]=jpg&filename[2]=php时：

$filename[count($filename)-1] 是$filename[1]

而end($filename)是传入的参数中最后一个$filename[2]

这里你把2换成0也是一样的，因此，我们传入如下参数时：
filename[1]=jpg&filename[2]=php，实际拼接进文件名的是php，接下来就是找文件了，可以看到文件名中混入了随机数，这里正常的思路应该是：预测随机数，获得文件名。

但是这里有一个unlink函数的绕过问题，也就是常说的先上传后删除的问题，unlink函数在遇到以下情况时不会删除文件：

1. name=xxx/../1.php(在Linux下可行，windows下因为也会处理路径API而被删除)
2. name=1.php/.  (这个在wonderkun师傅在的博客中说的很清楚了)
3. name=1.php:test （在windows下会生成一个1.php的空白文件)

在想了想随机数的攻击成本有点高之后，再加之开始打题的时间也比较晚，就去试着绕过unlink，最后传入的参数为：
filename[2]==/../test.php/. 

因为filename[0]会带入文件名，因此我没传，这样就会生成一个test.php文件。

而有关php去文件内容的地方，使用script标签以及php内的反引号去执行命令，就可以了。