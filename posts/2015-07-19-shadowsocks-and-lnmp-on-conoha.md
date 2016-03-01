title: 在 CentOS 上搭建 Shadowsocks 和 LNMP 过程及遇到的问题
categories: Tech
tags: [Linux, Shadowsocks]

这几天闲着蛋疼，折腾了一下 VPS。这玩意每次折腾都得烦死，但每次都忍不住地去折腾。

## 1. 过程

其实过程没什么好写的，网上到处都是教程。VPS 我用的 ConoHa 新加坡 1GB 内存 CentOS 6.6 32bit，下面是我参考的内容。

### 1.1 Shadowsocks

- [【倾力原创】史上最详尽Shadowsocks从零开始一站式翻墙教程](http://shadowsocks.blogspot.com/2015/01/shadowsocks.html)
- [Shadowsocks 使用说明](https://github.com/shadowsocks/shadowsocks/wiki/Shadowsocks-%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E)
- [Configuration via Config File](https://github.com/shadowsocks/shadowsocks/wiki/Configuration-via-Config-File)

### 1.2 LNMP

- [LNMP 安装](http://lnmp.org/install.html)
- [LNMP 目录](http://lnmp.org/faq/lnmp-software-list.html)
- [LNMP 添加虚拟主机](http://lnmp.org/faq/lnmp-vhost-add-howto.html)

## 2. 问题

安装 Shadowsocks 倒是没遇到什么问题，比较坑的主要是在安装 LNMP 之后，大致有以下几个问题。

### 2.1 LNMP 内存占用高

一开始系统选了 CentOS 7.1 x64，安装 LNMP 的时候图新鲜，MySQL 和 PHP 都选了最新的版本，结果最后 1GB 内存占用了 800MB（那时候都还没装 Shadowsocks）。其实 LNMP 官方文档的系统需求写得很清楚了：
> 128M 以上内存，Xen 的需要有 SWAP，OpenVZ 的另外至少要有 128MB 以上的 vSWAP 或突发内存（**小内存请勿使用 64 位系统**），**MySQL 5.6 及 MariaDB 10 必须 1G 以上内存**。

### 2.2 给非 root 用户添加 sudo 权限

一般肯定得新建一个用户，直接用 root 会比较危险，比如我们新建了一个叫 user 的用户，它所在的用户组叫也叫 user。user 用户默认是不可以用 sudo 的，所以先切到 root 用户，`cd /etc`、`ls -l` 之后可以找到一个叫 `sudoers` 的文件，这文件很牛逼，注意它权限是 `-r--r-----`，root 用户都只能读不能写，但这不妨碍我们去改变它的权限，`chmod u+w sudoers` 即可给它添加 root 用户对它的写权限，`vim sudoers` 打开，然后找到 `root    ALL=(ALL)       ALL`，在下面添加一行 `user ALL=(ALL) ALL`，`:wq` 保存并退出，别忘了 `chmod u-w sudoers` 把 root 用户的写权限去掉。这样再切回 user 用户就可以用 sudo 了。

### 2.3 文件权限

Linux 的文件权限一直没搞懂，这次这么一折腾似乎稍微明白了，说实话并不确定，如果我的理解没错的话，是这样的：

正如上一个问题里面出现的，`ls -l` 之后可以看到文件的权限，形如 `-r--r-----`。这东西有 10 位，第一位表示文件类型，比如这里 `-` 表示文件，如果是 `d` 则表示目录，之后的 9 位分为三段，每段 3 位，依次代表「所属用户」「所属组」「其他用户」对它的权限，3 位分别是 `r`、`w`、`x`，依次表示「读」「写」「执行」权限。权限后面可看到文件的「所属用户」和「所属组」。

比如 `-r--r-----   1 root      root        4024 Jul 18 19:13 sudoers`，这个文件所属用户是 root，所属组是 root，前面的权限表示：root 用户可以对它进行读操作，root 组的其他用户也可以对它进行读操作，非 root 组的用户不可以对它进行任何操作，如果你在 user 用户下试图用 vim 打开它会提示「Permission denied」。这个权限也可以表示为 `440`，计算方法是这样的：「读」是 4、「写」是 2、「执行」是 1，「无权限」是 0，加起来就行，这样只需要 3 个 0~7 的数字即可表示权限，如下表：

| 数字 | 权限   |
| --- | ----- |
| 0   | 无权限 |
| 1   | x     |
| 2   | w     |
| 3   | wx    |
| 4   | r     |
| 5   | rx    |
| 6   | rw    |
| 7   | rwx   |

这样要对 `sudoers` 文件添加 root 用户对它的写权限就可以执行这个命令 `chmod 640 sudoers`，而上一个问题中所用的是这个命令 `chmod u+w sudoers`，当然也是 OK 的，`u+w` 中 3 个字符连起来表示给文件「所属用户」「添加」「写权限」，规则如下表：

| 字符 | 含义            |
| --- | ---------------|
| a   | 所有权限/所有用户 |
| u   | 用户            |
| g   | 用户组          |
| o   | 其他用户         |

| 字符 | 含义       |
| --- | ---------- |
| +   | 添加（权限） |
| -   | 去除（权限） |
| =   | 等于（权限） |

### 2.4 git clone 失败

可能因为当前用户对当前目录没有写权限，我当时用 user 用户在 `/home/wwwroot`（即 nginx 默认的网站目录 `default` 所在的那个文件夹）试图 `git clone`，提示没权限，折腾了半天以为因为 GitHub 那边公钥没填好，后来才发现 `wwwroot` 目录是 `root:root` 的，且权限为 `drwxr-xr-x`，也就是说非 root 用户只能读和执行，不能写，即使是 root 组的其他用户。最后怎么解决的在后面的问题里面讲。

### 2.5 vhost 创建虚拟主机之后 403 Forbidden

这个问题归根到底也是文件权限问题，我是先在 user 用户下 git clone 了一个目录在 user 主目录，假设目录名为 `test`，属主和属组都是 user，`sudo lnmp vhost add` 之后，指定了 `test` 为 `test.example.com` 域名的主目录，命令自动把 `test` 目录及其内容文件的属主和属组都改成了 www，`test` 目录权限为 `drwxr-xr-x`，按理说 nginx 是可以访问它的，但是结果是 `403 Forbidden`，后来发现 user 主目录本身权限是 `drwx------`，这才导致 403。所以建议把虚拟主机主目录都放到 `/home/wwwroot`，这个目录虽然是 `root:root` 的，但权限是 `drwxr-xr-x`，www 用户可读。

### 2.6 user 用户无法更改虚拟主机目录中的文件

上一个问题中说到 `sudo lnmp vhost add` 之后，虚拟主机主目录是 `www:www` 的，权限为 `drwxr-xr-x`，所以 user 是没法更改内容的，但是平时为了安全起见都用 user 用户，改个网页什么的也 sudo 也太麻烦了吧，最后我的解决办法是，把 `test` 目录属主改为 user，属组保持原来 www 不变，用命令 `chown user:www -R test`，保持文件权限不变，即 `drwxr-xr-x`，这样 user 用户就可以自由读写，nginx 也可以读而不会导致 403。这样改的话，我猜想如果以后运行 PHP 需要读写文件肯定会权限不够，不过到时候把权限改成 775 应该就行了。

### 2.7 虚拟主机目录中的 `.user.ini` 文件删不掉

有时候某个虚拟主机不想要了，`sudo lnmp vhost del` 删了之后还没完，还得自己把目录删除，就拿上面的 `test` 目录为例，这里面有个 `.user.ini` 文件直接删是怎么都删不掉的，它属主和属组都是 root，但即使用 `sudo rm .user.ini` 还是删不掉。就在差点就准备把 VPS 删了不玩了的时候，去看了 lnmp 命令的脚本，`vim /bin/lnmp`，发现在创建虚拟主机的时候，建立 `.user.ini` 文件后，执行了 `chmod 644 ${vhostdir}/.user.ini`、`chattr +i ${vhostdir}/.user.ini` 这两个命令，查了一下，原来罪魁祸首是第二个命令，`chattr` 命令可以改变文件的属性而不是权限，这里的 `+i` 作用是「设定文件不能被删除、改名、设定链接关系，同时不能写入或新增内容」，所以即使是 root 用户也没办法删除它。这里 `+`、`-`、`=` 的含义和 `chmod` 时用到的含义相同，第二个字符规则如下表：

| 字符 | 含义 |
| --- | --- |
| A   | 文件或目录的 atime (access time) 不可被修改 (modified), 可以有效预防例如手提电脑磁盘 I/O 错误的发生。 |
| S   | 硬盘 I/O 同步选项，功能类似 sync。 |
| a   | 即 append，设定该参数后，只能向文件中添加数据，而不能删除，多用于服务器日志文件安全，只有 root 才能设定这个属性。 |
| c   | 即 compresse ，设定文件是否经压缩后再存储。读取时需要经过自动解压操作。 |
| d   | 即 no dump，设定文件不能成为 dump 程序的备份目标。 |
| i   | 设定文件不能被删除、改名、设定链接关系，同时不能写入或新增内容。i 参数对于文件 系统的安全设置有很大帮助。 |
| j   | 即 journal，设定此参数使得当通过 mount 参数：data=ordered 或者 data=writeback 挂载的文件系统，文件在写入时会先被记录（在journal中）。如果 filesystem 被设定参数为 data=journal，则该参数自动失效。|
| s   | 保密性地删除文件或目录，即硬盘空间被全部收回。 |
| u   | 与s相反，当设定为u时，数据内容其实还存在磁盘中，可以用于undeletion。 |

对于这个 `.user.ini` 文件，只要 `sudo chattr -i .user.ini` 一下就能删了。用 `lsattr` 命令可以查看相应文件的属性。

## 3. 结尾

就这么多了，以后每折腾一阶段都要去备份一下 VPS，这玩意出问题太麻烦了。

关于 `chmod`、`chown`、`chattr` 的更多资料，见维基百科：[chattr](https://en.wikipedia.org/wiki/Chattr) [chmod](https://en.wikipedia.org/wiki/Chmod) [chown](https://en.wikipedia.org/wiki/Chown)。

## 4. 参考资料

- [CentOS下添加sudo用户](http://www.centoscn.com/CentOS/help/2014/0815/3499.html)
- [LNMP 常见问题](http://lnmp.org/faq.html)
- [Linux学习笔记：用户管理和权限控制](http://blog.csdn.net/boybruce/article/details/17198601)
- [（总结）Linux的chattr与lsattr命令详解](http://www.ha97.com/5172.html)
