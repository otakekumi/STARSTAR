title: 笔记：PHP Internal 
date: 2018-02-03 23:36:41
tags: ['PHP安全相关']


# PHP的生命周期

PHP初期是作为单进程的CGI来运行的，因此不需要考虑线程安全问题。随着使用多线程模式的软件系统越来越多，php内核中形成了一个新的抽象层：TSRM（Thread Safe Resource Management）

## 线程安全与非线程安全

### Thread-Safe Data Pools
在扩展的module init过程中，扩展可以使用ts\_allocate\_id来申请资源。

```c
typedef struct {
    int sampleint;
    char *samplestring;
} php_sample_globals;
int sample_globals_id;
 
PHP_MINIT_FUNCTION(sample)
{
    ts_allocate_id(&sample_globals_id,
        sizeof(php_sample_globals),
        (ts_allocate_ctor) php_sample_globals_ctor,
        (ts_allocate_dtor) php_sample_globals_dtor);
    return SUCCESS;
}
```

但一个请求访问数据段的时候，扩展从TSRM层请求当前线程的资源池，以ts\_allocate\_id返回的资源ID来获取偏移量。

### 当不在线程环境时
因为在PHP的线程安全构建中访问全局资源涉及到在线程数据池查找对应的偏移量，这是一些额外的负载。因此它比对应的非线程方式要慢一些（比如直接从真实的全局变量地址中取出数据）。
### 访问全局变量
在创建扩展时，标准文件包含集合中已经包含了条件定义的ZTS预处理标记。当PHP以线程安全方式构建时，这个值会被自动定义，只有在PHP以线程安全方式编译时，才会存在线程安全池。
### 即使不需线程也要考虑线程
正常的PHP构建默认是关闭线程安全的，只有在被构建的SAPI明确需要线程安全或者线程安全在./configure阶段显式的打开时，才会以线程安全方式构建。

当线程安全启用时，一个名为tsrm_ls的指针被增加到很多的内部函数原型中。这个指针允许PHP区分不同线程的数据。

在ZTS开启时，展开如下：

```c
#define TSRMLS_D     void ***tsrm_ls
#define TSRMLS_DC     , void ***tsrm_ls
#define TSRMLS_C     tsrm_ls
#define TSRMLS_CC     , tsrm_ls
```

```c
int php_myext_action(int action_id, char *message TSRMLS_DC);
php_myext_action(42, "The meaning of life" TSRMLS_CC);
```

可以看到，在非ZTS构建下，代码看到的是int,char * 。在ZTS构建下，原型则包括三个参数:int,char * ,void ***。

# PHP变量在内核中的实现

## 2.1变量的类型
PHP在内核中通过zval这个结构体来存储变量，它的定义在Zend/zend.h文件里，如下：

```c
struct _zval_struct {
    zvalue_value value; /* 变量的值 */
    zend_uint refcount__gc;
    zend_uchar type;    /* 变量当前的数据类型 */
    zend_uchar is_ref__gc;
};
typedef struct _zval_struct zval;
 
//在Zend/zend_types.h里定义的：
typedef unsigned int zend_uint;
typedef unsigned char zend_uchar;
```

zval里的refcout\_\_gc是zend\_unit类型，也就是unsigned int类型，is\_ref\_\_gc和type则是unsigned char型的。

保存变量值的value则是zvalue\_value类型（php5），它是一个union，同样定义在了Zend/zend.h：

```c
typedef union _zvalue_value {
    long lval;  /* long value */
    double dval;    /* double value */
    struct {
        char *val;
        int len;
    } str;
    HashTable *ht;  /* hash table value */
    zend_object_value obj;
} zvalue_value;
```

在这个基础上，PHP实现了八种数据类型：

1. IS_NULL
2. IS_BOOL
3. IS_LONG
4. IS_DOUBLE
5. IS_STRING
6. IS_ARRAY
7. IS_OBJECT
8. IS_RESOURCE

其中，要注意的是，对象除了存储复合数据以外，还需要保存：方法，访问权限，类常量以及其他的处理逻辑。

zval的type成员的值便是这八个之一。内核通过检测这个成员值来判断数据类型，如果要判断一个变量的类型，则读取type成员的值即可:

```c
void describe_zval(zval *foo)
{
    if (foo->type == IS_NULL)
    {
        php_printf("这个变量的数据类型是： NULL");
    }
    else
    {
        php_printf("这个变量的数据类型不是NULL，这种数据类型对应的数字是： %d", foo->type);
    }
}   
```

> 虽然这种实现是正确的，但不建议这么做。

PHP内核以后可能会修改变量的实现方式，因此检测type的方式以后可能会失效。为了解决这个问题，zend在头文件中定义了大量的宏，供我们检测、操纵变量。比如使用Z\_TYPE\_P()来改写上面那个程序：

```c
void describe_zval(zval *foo)
{
    if ( Z_TYPE_P(foo) == IS_NULL )
    {
        php_printf("这个变量的数据类型是： NULL");
    }
    else
    {
        php_printf("这个变量的数据类型不是NULL，这种数据类型对应的数字是： %d", foo->type);
    }
}
```
> php_printf()函数是php内核对printf函数的一层封装


以_P结尾的宏的参数大多是* zval型变量。此外还有Z
\_TYPE和Z\_TYPE\_PP，前者是zval，后者是**zval。这三个宏的实现在Zend/zend_operations.h:

```c
#define Z_TYPE(zval)        (zval).type
#define Z_TYPE_P(zval_p)    Z_TYPE(*zval_p)
#define Z_TYPE_PP(zval_pp)  Z_TYPE(**zval_pp)
```

在以上知识的基础上，gettype的函数实现为:

```c
PHP_FUNCTION(gettype)
{
    //这个arg间接指向就是我们传给gettype函数的参数。是一个zval**结构
    //所以我们要对他使用__PP后缀的宏。
    zval **arg;
 
    //这个if的操作主要是让arg指向参数～
    if (zend_parse_parameters(ZEND_NUM_ARGS() TSRMLS_CC, "Z", &arg) == FAILURE) {
        return;
    }
     
    //调用Z_TYPE_PP宏来获取arg指向zval的类型。
    //然后是一个switch结构，RETVAL_STRING宏代表这gettype函数返回的字符串类型的值
    switch (Z_TYPE_PP(arg)) {
        case IS_NULL:
            RETVAL_STRING("NULL", 1);
            break;
 
        case IS_BOOL:
            RETVAL_STRING("boolean", 1);
            break;
 
        case IS_LONG:
            RETVAL_STRING("integer", 1);
            break;
 
        case IS_DOUBLE:
            RETVAL_STRING("double", 1);
            break;
     
        case IS_STRING:
            RETVAL_STRING("string", 1);
            break;
     
        case IS_ARRAY:
            RETVAL_STRING("array", 1);
            break;
 
        case IS_OBJECT:
            RETVAL_STRING("object", 1);
            break;
 
        case IS_RESOURCE:
            {
                char *type_name;
                type_name = zend_rsrc_list_get_rsrc_type(Z_LVAL_PP(arg) TSRMLS_CC);
                if (type_name) {
                    RETVAL_STRING("resource", 1);
                    break;
                }
            }
 
        default:
            RETVAL_STRING("unknown type", 1);
    }
}       
```

## 2.2变量的值

正如Z\_TYPE\_P此类宏一样，PHP内核同样提供了基础宏方便我们对变量的值进行操作。
为了针对不同的数据类型进行操作，内核又定义了不同的宏，比如对IS\_BOOL型的Z\_BVAL，Z\_BVAL\_P，Z\_BVAL\_PP。针对IS\_DOUBLE的Z\_DVAL，Z\_DVAL\_P，Z\_DVAL\_PP。

ARRAY变量的值实质是存储在C语言的HashTable中的，我们可以用ARRAVAL组合宏(z\_ARRVAL,Z\_ARRVAL\_P,Z\_ARRVAL\_PP)来访问数组的值。

有关值操作的宏定义都在Zend/zend_operations.h中。

## 2.3创建PHP变量

在创建PHP变量时，不直接使用C语言的malloc函数，而是使用宏MAKE_STD_ZVAL(pzv)，这个宏会申请一块地址赋给pzv，并初始化refcount和is\_ref属性。

在申请完空间后，便可以对这个zval进行赋值操作。内核提供了以下宏供我们使用：

| 新宏 	|   其他宏的实现方法	|
| ----	| -----:	|
|	ZVAL_NULL(pvz); **(注意这个Z和VAL之间没有下划线！)**|Z_TYPE_P(pzv) = IS_NULL;**(IS_NULL型不用赋值，因为这个类型只有一个值就是null，^_^)**|
|ZVAL_BOOL(pzv, b); **(将pzv所指的zval设置为IS_BOOL类型，值是b)**|Z_TYPE_P(pzv) = IS_BOOL; Z_BVAL_P(pzv) = b ? 1 : 0;|
|ZVAL_TRUE(pzv); **(将pzv所指的zval设置为IS_BOOL类型，值是true)**		|ZVAL_BOOL(pzv, 1);|
|ZVAL_FALSE(pzv); **(将pzv所指的zval设置为IS_BOOL类型，值是false)**			|ZVAL_BOOL(pzv, 0);			|
|ZVAL_LONG(pzv, l); **(将pzv所指的zval设置为IS_LONG类型，值是l)**			|Z_TYPE_P(pzv) = IS_LONG;Z_LVAL_P(pzv) = l;|
|ZVAL_DOUBLE(pzv, d); **(将pzv所指的zval设置为IS_DOUBLE类型，值是d)**|Z_TYPE_P(pzv) = IS_DOUBLE;Z_DVAL_P(pzv) = d;|
|	ZVAL_STRINGL(pzv,str,len,dup);**(下面单独解释)**		|Z_TYPE_P(pzv) = IS_STRING;Z_STRLEN_P(pzv) = len;if (dup) {Z_STRVAL_P(pzv) =estrndup(str, len + 1);} else{Z_STRVAL_P(pzv)= str;}			|
|ZVAL_STRING(pzv, str, dup);			|ZVAL_STRINGL(pzv, str,strlen(str), dup);|
|ZVAL_RESOURCE(pzv, res);			|	Z_TYPE_P(pzv) = IS_RESOURCE;Z_RESVAL_P(pzv) = res;|


## 2.4变量的存储方式

在PHP中，用户在PHP中定义的变量我们都可以在一个HashTable中找到，当PHP中定义了一个变量，内核会自动把它的信息存储到一个用HashTable实现的符号表中。

全局作用域的符号表是在调用RINIT方法前创立的，并在RSHUTDOWN后销毁。

当用户在PHP中调用一个一个函数或者类的时候，内核会创建一个新的符号表并激活之，这也就是为什么我们无法在函数中使用函数外定义的变量的原因。

打开Zend/zend\_globals.h文件，看一下\_zend\_execution\_globals结构体，会在其中发现两个element：

```c
struct _zend_executor_globals {
    ...
    HashTable symbol_table;
    HashTable *active_symbol_table;
    ...
};
```
其中，symbol\_table元素可以通过EG宏访问，它代表着PHP的全局变量。active\_symble\_table则代表的是处于当前作用域的变量符号表。

以以下PHP代码作为实例：

```php
<?php   $foo = "bar"; ?>
```
在内核中的实现便是:

```c
{
	zval *fooval;
	MAKE_STD_ZVAL(fooval);
	ZVAL_STRING(fooval,"bar",1);
	ZEND_SET_SYMBOL(EG(active_symbol_table),"foo",fooval);
}
```
即：先声明一个zval指针，并申请一块内存。再通过ZVAL\_STRING将值设置为bar，最后一行的作用就是将这个zval加到当前的符号表中，并将其label设置定义成foo，这样便可以在代码里使用$foo.

## 2.5变量的检索
PHP内核中主要通过zend_hash_find函数来找到某个作用域下的用户已经定义好的变量.它是内核提供的操作HashTable的API之一.

```c
{
    zval **fooval;
 
    if (zend_hash_find(
            EG(active_symbol_table), //这个参数是地址，如果我们操作全局作用域，则需要&EG(symbol_table)
            "foo",
            sizeof("foo"),
            (void**)&fooval
        ) == SUCCESS
    )
    {
        php_printf("成功发现$foo!");
    }
    else
    {
        php_printf("当前作用域下无法发现$foo.");
    }
}       
```
HashTable结构并不只是用于存储PHP语言里的变量，其他很多地方都在应用HashTable。一个HashTable有很多元素，在内核里叫做bucket。每个bucket的大小是固定的。如果想在bucket中存储数据，最好是先申请一块内存保存数据，然后在bucket中保存这个指针。

## 2.6类型转换

作为弱类型语言，类型转换是一个很不可忽视的方面，在内核中提供了许多函数用于实现类型转换，这一类函数有一个统一的形式:convert\_to\_*().

```c
//将任意类型的zval转换成字符串
void change_zval_to_string(zval *value)
{
    convert_to_string(value);
}
 
//其它基本的类型转换函数
ZEND_API void convert_to_long(zval *op);
ZEND_API void convert_to_double(zval *op);
ZEND_API void convert_to_null(zval *op);
ZEND_API void convert_to_boolean(zval *op);
ZEND_API void convert_to_array(zval *op);
ZEND_API void convert_to_object(zval *op);
 
ZEND_API void _convert_to_string(zval *op ZEND_FILE_LINE_DC);
\#define   convert_to_string(op) if ((op)->type != IS_STRING) { _convert_to_string((op) ZEND_FILE_LINE_CC); }
        
```

# 3 内存管理
脚本语言和编译型语言最根本的区别可能就在内存管理上，现在越来越多的语言不允许用户直接操作内存，而是由虚拟机来负责内存的分配以及回收，如C#，Java，PHP等等。

## 3.1 内存管理

### Free the Mallocs
 
每个平台操作内存的方式都差不多是两个方面，一是负责申请，二是负责释放。如果一个内存块没有释放，并且所有者应用程序也永远不再使用它了，那么就称其为“内存泄漏”。小量，短时间的内存泄漏是无关紧要的，但是在使用Apache此类长时间运行的web服务器时，即使是小量的内存泄漏，累积多了也会使系统的资源消耗殆尽。

### 错误处理

为了实现从用户端"跳出"，需要使用一种方法来完全”跳出“一个活动请求。这个功能是在内核中实现的：在一个请求的开始设置一个“跳出”地址，然后在任何die()或者exit()调用或在任何关键错误（E\_ERROR）时执行一个longjmp()以跳转到该地址。
以下是PHP中使用函数的使用原理：

```c
void call_function(const char *fname, int fname_len TSRMLS_DC){
    zend_function *fe;
    char *lcase_fname;
    /* php函数的名字是大小写不敏感的
     * 我们可以在function tables里找到他们
     * 保存的所有函数名都是小写的。
     */
    lcase_fname = estrndup(fname, fname_len);
    zend_str_tolower(lcase_fname, fname_len);
 
    if (zend_hash_find(EG(function_table),lcase_fname, fname_len + 1, (void **)&fe) == SUCCESS)
    {
        zend_execute(fe->op_array TSRMLS_CC);
    }
    else
    {    
        php_error_docref(NULL TSRMLS_CC, E_ERROR,"Call to undefined function: %s()", fname);
    }
    efree(lcase_fname);
}
```
当php_error_docref这个函数被调用时，便会触发内核中的错误处理机制，根据错误级别来决定是否调用longjmp来终止当前请求并退出call_function()，从而efree函数便永远不会执行。

其实php\_error\_docref()函数就相当于PHP语言里trigger\_error()函数.它的第一个参数是一个将被添加到docref的可选的文档引用第三个参数可以是E_*家族常量，用于指示错误的严重程度。

### Zend内存管理器
在上面的“跳出”请求期间解决内存泄漏的方案之一是：使用Zend内存管理(Zend Merory Manager，简称ZendMM层、ZMM)层。内核的这一部分是非常类似于操作系统的内存管理功能--分配内存给调用程序。区别在于，它处于进程空间中非常低的位置而且是“请求感知”的；这样一来，当一个请求结束时，它能够执行与OS在一个进程终止时相同的行为。就是说，它会隐式的释放所有的为该请求占用的内存。

除了提供隐式的内存清楚功能之外，ZendMM还能够根据php.ini中merory_limit设置来控制每一次内存请求行为。

## 3.2 引用计数

对于PHP这种需要同时处理多个请求的程序来说，申请和释放内存的时候应该慎之又慎。除了安全的申请和释放内存之外，还应该做到内存的最小化使用。

以下面的PHP代码为例子:

```c
<?php
$a = 'Hello World';
$b = $a;
unset($a);   
```
在这段代码中，先是对变量a赋值，再将a赋值给b，在PHP中，考虑到负载问题，PHP中的变量的名称和值在内核中是分开存放的，变量的名字a存放在符号表中，而值通过一个zval结构保存，而现在将a赋值给b则是让两者指向完全相同的内容。

先看一下其实现：

```c
zval *helloval;
MAKE_STD_ZVAL(helloval);
ZVAL_STRING(helloval, "Hello World", 1);
zend_hash_add(EG(active_symbol_table), "a", sizeof("a"),&helloval, sizeof(zval*), NULL);
zend_hash_add(EG(active_symbol_table), "b", sizeof("b"),&helloval, sizeof(zval*), NULL);  
```
乍一看，当unset被调用时，会直接释放a的内存，如果不加以处理，便会引发逻辑错误。现在看一下zval的四个成员:
value、type、is\_ref\_\_gc、refcount\_\_gc。当一个变量被第一次创建时，refcount\__gc成员被初始化为1，当这个变量被赋值给变量时，refcount\_\_gc成员会变成2，因为此时有两个变量在使用这个zval结构。其实现如下:

```c
zval *helloval;
MAKE_STD_ZVAL(helloval);
ZVAL_STRING(helloval, "Hello World", 1);
zend_hash_add(EG(active_symbol_table), "a", sizeof("a"),&helloval, sizeof(zval*), NULL);
ZVAL_ADDREF(helloval); //这句很特殊，我们显式的增加了helloval结构体的refcount
zend_hash_add(EG(active_symbol_table), "b", sizeof("b"),&helloval, sizeof(zval*), NULL);    
```

回到上面的php代码，对$aunset便是将对应的zval结构的refcount\_\_gc的值变为1.

### 写时复制机制

当面对以下PHP代码时：

```php
<?php 
$a = 1;
$b = $a;
$b += 5;
```
可以看出，我们希望执行后的a仍然为1，b为6，在refcount\_\_gc大于1时，则为这个变化的变量从原zval结构复制一份新的zval出来，并改变其值。以下是其实现:

```c

zval *get_var_and_separate(char *varname, int varname_len TSRMLS_DC)
{
    zval **varval, *varcopy;
    if (zend_hash_find(EG(active_symbol_table),varname, varname_len + 1, (void**)&varval) == FAILURE)
    {
        /* 如果在符号表里找不到这个变量则直接return */
        return NULL;
    }
 
    if ((*varval)->refcount < 2)
    {   
        //如果这个变量的zval部分的refcount小于2，代表没有别的变量在用，return
        return *varval;
    }
     
    /* 否则，复制一份zval*的值 */
    MAKE_STD_ZVAL(varcopy);
    varcopy = *varval;
     
    /* 复制任何在zval*内已分配的结构*/
    zval_copy_ctor(varcopy);
 
    /* 从符号表中删除原来的变量
     * 这将减少该过程中varval的refcount的值
     */
    zend_hash_del(EG(active_symbol_table), varname, varname_len + 1);
 
    /* 初始化新的zval的refcount，并在符号表中重新添加此变量信息，并将其值与我们的新zval相关联。*/
    varcopy->refcount = 1;
    varcopy->is_ref = 0;
    zend_hash_add(EG(active_symbol_table), varname, varname_len + 1,&varcopy, sizeof(zval*), NULL);
     
    /* 返回新zval的地址 */
    return varcopy;
}      
```

### Change on Write
在进行以下赋值时:

```php
<?php
$a = 1;
$b = &$a;
$b += 5;
?>
```

此时，b是对a的引用，因此对b的更改会直接影响到a变量，也就无需上面那样再复制一份zval结构了。

而zval的is\_ref\_\_gc则是检测是否是一个用户在PHP语言中定义的引用。在执行第三条语句时，内核再次检查b变量的zval以确定是否需要复制一份新的zval结构。
实现如下：

```c
if((*varval)->is_ref || (*varval)->refcount < 2){
	return *varval;
}
```
加上这句，上面的get\_var\_and\_separate才是完整的。

# 4 动手编译PHP

## 4.1 
之前说过，PHP编译前的configure有两个特殊的选项，对于开发扩展是很有帮助的

###  --enable-debug
顾名思义，它的作用是激活调试模式。它将激活PHP源码中几个非常关键的函数，最典型的功能便是在每一个请求结束后给出这一次请求中内存的泄漏情况。

### --enable-maintainer-zts
第二个重要的参数便是激活php的线程安全机制(Thread Safe Resource Manager(TSRM)/Zend Thread Safety(ZTS))，使我们开发出的程序是线程安全的。对于TRSM的介绍大家可以参考第一章的介绍，在平时的开发中，建议打开这个选项。

### --enable-embed
其实还有一个选项比较重要，那就是enable-embed，它主要用在你做php的嵌入式开发的场景中。平时我们把php作为apache的一个module进行编译，得到libphp5.so，而这个选项便使php编译后得到一个与我们设定的SAPI相对应的结果。







