title: CentOS 上安装 shadowsocks-manyuser 实现 shadowsocks 多人共享平台

## 1. 创建数据库

首先创建数据库 `shadowsocks`，然后下载 [https://raw.githubusercontent.com/fanyueciyuan/eazy-for-ss/master/Our-Private-Panel/shadowsocks.sql](https://raw.githubusercontent.com/fanyueciyuan/eazy-for-ss/master/Our-Private-Panel/shadowsocks.sql)，做一定的修改，参考下面命令：

```sh
username="登录网站用户名"
password="登录网站明文密码"
My_Domain="自己的ip或者域名"
ss_mypassword="ss连接密码"
Panel_Admin_Passwd=`echo -n "$password"|md5sum|cut -d ' ' -f1`
sed -i "s/25d55ad283aa400af464c76d713c07ad/$Panel_Admin_Passwd/" shadowsocks.sql
sed -i "s/Our_Private_Panel_Domain/$My_Domain/" shadowsocks.sql
sed -i "s/Our_Private_Panel/$username/" shadowsocks.sql
sed -i "s/My_Passwd/$ss_mypassword/" shadowsocks.sql
```

改完后，导入数据库，并重启 mysql。

（更推荐用外部数据库，在更换服务器时候比较方便）

## 2. 安装 shadowsocks-manyuser

安装依赖：

```sh
yum -y install epel-release
yum -y update epel-release
yum -y install git python-setuptools m2crypto supervisor
easy_install pip
pip install cymysql
```

下载 shadowsocks-manyuser：

```sh
git clone -b manyuser https://github.com/mengskysama/shadowsocks.git
cd shadowsocks/shadowsocks
```

修改 `Config.py` 里的数据库信息和 `config.json` 里的加密方式，然后执行下面命令方便后面看的清楚：

```sh
mkdir -p /etc/shadowsocks-manyuser
mv * /etc/shadowsocks-manyuser
cd ../..
rm -rf shadowsocks
```

在 `/etc/supervisord.conf` 结尾添加：

```sh
[program:shadowsocks-manyuser]
command=python /etc/shadowsocks-manyuser/server.py -c /etc/shadowsocks-manyuser/config.json
autostart=true
autorestart=true
```

最后执行：

```sh
echo 'ulimit -n 51200' >>  /etc/default/supervisor
service supervisord restart
supervisorctl reload
```

大功告成！

（之后可以装 [ss-panel](https://github.com/orvice/ss-panel) 或者 [moeSS](https://github.com/wzxjohn/moeSS) 前端来进行管理）

## 3. 参考资料

- [ss多服务器多用户搭建简要备忘](http://www.fanyueciyuan.info/fq/ss-panel-manyuser.html)
- [【倾力原创】史上最详尽Shadowsocks从零开始一站式翻墙教程](http://shadowsocks.blogspot.hk/2015/01/shadowsocks.html)
