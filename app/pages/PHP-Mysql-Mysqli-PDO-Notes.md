title: 笔记：PHP Mysql Mysqli PDO Extensions
date: 2018-02-03 23:43:54
tags: ['PHP安全相关']

# Mysql,mysqli,PDO扩展学习笔记
当考虑到MySQL数据库服务器的时候，有主要的三种API可供选择，分别是：

1.PHP的MySQL扩展

2.PHP的mysqli扩展

3.PHP数据对象（PDO）

## PHP的MySQL扩展

这是早期允许PHP应用与MySQL数据库服务器进行交互的扩展，MySQL扩展提供了一个面向过程的接口，现在已经不推荐使用MySQL扩展去对MySQL数据库服务器进行交互，推荐使用mysqli扩展加以代替。

## PHP的mysqli扩展

mysqli扩展，也被称为mysql增强扩展，相比于MySQL扩展的提升主要有：

1.面向对象接口

2.prepared语句支持

3.多语句执行支持

4.事物支持

5.增强的调试支持

6.嵌入式服务扩展

mysqli扩展在提供了面向对象接口的同时也提供了一个面向过程的接口，mysqli扩展是通过使用PHP扩展框架构架的，它的源代码在ext／mysqli下。

## PHP数据对象（PDO）

PHP数据对象，是PHP应用中一个数据库抽象层规范。PDO提供了一个统一的API接口，在使用中，可以不用过多考虑目标服务器的系统类型，可以在任何时候无缝切换数据库服务器。

其他数据库抽象层的例子为：Java中的JDBC，perl中的DBI

PDO提供了一个干净简单，可移植性强的API，主要缺点为无法使用后期MySQL数据库的所有高级特性，比如多语句执行，但是随着后期PHP的新版本发布，也支持数据库高级特性。

PDO也是基于PHP扩展框架构建的，其源码在ext／pdo下。

## PDO的MySQL数据库驱动器

PDO的MySQL驱动并不是一套API，PDO的MySQL驱动位于PDO的下层，当直接调用PDO的API的时候，PDO使用PDO的MySQL扩展完成与MySQL服务器端的交互。

PDO的MySQL驱动并不是PDO的唯一驱动，其他的PDO驱动包括Firebird驱动，PostgreSQL驱动等。

## PHP的MySQL Native驱动

为了和MySQL数据库服务器进行交互，mysql扩展，mysqli扩展，PDO MySQL驱动都实现了必要的协议的底层库。以前可用的库只有MySQL客户端和libmysql，然而libmysql是早期为C程序设计的，因此MySQL Native作为libmysql的一个针对PHP应用的修改版本开发。
MySQL Native驱动是基于PHP扩展框架实现的，源代码为位于etc／mysqlnd下。

## 数据库抽象层
使用数据库抽象层，便意味着当进行数据库迁移的时候，无需更改大量代码。

当不使用数据库抽象层时，PHP通过扩展直接与MySQL数据库服务器进行交互，比如MySQL扩展的mysql_connect()便是PHP直接与MySQl进行交互。

当使用数据库抽象层，同样是connect()方法，通过数据库抽象层，便能使用mysql_connect(),ora_connect()这些方式去与数据库服务器进行匹配，因此对于使用者来说，便不需要考虑数据库的具体类型。

