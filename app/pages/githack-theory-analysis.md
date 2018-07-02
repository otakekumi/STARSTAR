title: GitHack Theroy Analysis
date: 2017-08-04 21:35:52
tags: ['杂项']


在进行GitHack的运行机制分析之前，需要先了解.git目录的组成结构。

.git目录由一下目录和文件组成:
> hooks:这个目录存放一些shell脚本，可以设置特定的git命令后触发相应的脚本；在搭建gitweb系统或其他git托管系统会经常用到hook script> 
> 
> info:包含仓库的一些信息> 
> 
> logs:保存所有更新的引用记录> 
> 
> objects:所有的Git对象都会存放在这个目录中，对象的SHA1哈希值的前两位是文件夹名称，后38位作为对象文件名> 
> 
> refs:这个目录一般包括三个子文件夹，heads、remotes和tags，heads中的文件标识了项目中的各个分支指向的当前commit> 
> 
> COMMIT_EDITMSG:保存最新的commit message，Git系统不会用到这个文件，只是给用户一个参考> 
> 
> config:这个是GIt仓库的配置文件> 
> 
> description:仓库的描述信息，主要给gitweb等git托管系统使用> 
> 
> index:这个文件就是我们前面提到的暂存区（stage），是一个二进制文件> 
> 
> HEAD:这个文件包含了一个档期分支（branch）的引用，通过这个文件Git可以得到下一次commit的parent> 
> 
> ORIG_HEAD:HEAD指针的前一个状态
明白这些基本组成后，可以发现，与还原代码内容密切相关的文件夹是objects文件夹，该文件夹的完整性直接影响GitHack还原的效果。

Freebuf上给出的原理比较简洁，我稍微扩充下（虽然感觉没啥卵用？）

&nbsp;

所以大概的思路就是通过.git/index文件找出与文件对应的hash值以及其原本路径和文件名，再进入.git/objects目录下还原其代码。

相关知识点在这个链接下：[git object details](https://www.kernel.org/pub/software/scm/git/docs/user-manual.html#object-details)

实际上查看objects文件夹，我们可以知道这些内容是经过加密，根据链接中的意思，objects是把文件内容进行deflate压缩后再进行存储的，我们只需要使用deflate解压该部分内容便可以获得原本的内容。

python中有zlib库，假设data为deflate压缩后的内容，zlib.decompress(data)便可以获得正常的内容，这里做个试验:

![](http://www.meizj.com.cn/wp-content/uploads/2017/08/3.png)

可以看到，这一块的文件内容是还原成功地，也就是说可以通过zlib库的decompress方法来还原objects下的内容。

接下来就通过看githack的源码来进行分析：

![](http://www.meizj.com.cn/wp-content/uploads/2017/08/1.png)

这一块内容总结就是分析index文件，将hash值与文件结构相对应。

![](http://www.meizj.com.cn/wp-content/uploads/2017/08/4.png)

可以看到，这里也是使用zlib库的decompress方法来还原数据。

至此，githack还原.git文件的方法已经清楚了

&nbsp;