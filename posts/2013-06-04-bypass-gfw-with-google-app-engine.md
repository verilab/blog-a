title: （已失效）使用 Google App Engine 翻墙
categories: Tech
tags: [GAE, GoAgent]


## 1. 登陆 App Engine

打开 [Google App Engine](http://appengine.google.com/) 网站。使用谷歌帐号登陆，如果没有谷歌账号请注册一个，注册步骤在此不一一阐述，非常简单。

## 2. 创建新的应用

登陆之后出现「Welcome to Google App Engine」页面，点击「Create Application」开始创建新应用。

在 Application Identifier 文本框输入新应用的名称，点击「Check Availability」检查是否可用。Application Title 文本框随便输入文字。两处输入完成后点击「Create Application」即可完成应用的创建。
（注释：每个谷歌帐号最多创建 10 个应用）

创建完成后出现「Application Registered Successfully」页面，建议先不要将本页面关闭，因为待会儿会用到刚刚创建的应用名称，如果你能清楚的记住应用名称，那就可以关闭。

## 3. 使用 goagent

前往 [https://github.com/goagent/goagent](https://github.com/goagent/goagent) 下载最新版本的 `goagent`，下载完成后，解压到一个不容易被自己误删的地方。使用文本编辑器打开解压后文件夹中 `local` 文件夹里的 `proxy.ini` 文件，将第 8 行 `appid ＝ ` 后面的初始应用名称改成刚才创建的应用的名称，保存并关闭文件。

下面的步骤 Windows 系统和 OS X 会有一些区别，我会分开讲。

### Windows

运行 `goagent` 文件夹中 `server` 文件夹里的 `uploader.bat` 文件，根据提示输入 appid（即刚才创建的应用名称）、Gmail 帐号、密码来上传服务端程序。上传完成后，运行 `goagent` 文件夹中 `local` 文件夹里的 `goagent.exe` 程序，不要关闭命令提示符窗口，可以点击屏幕右下托盘中的 goagent 图标来最小化。

### OS X

上传 `goagent` 服务段程序以前，你必须先安装 `gevent`，而安装 `gevent` 的前提条件是你已经安装 `xcode` 或者 `gcc-4.2`。如果 `greenlet` 版本过低会导致 `gevent` 装不上，请在终端输入以下命令安装 `greenlet-0.4.0`：

```sh
curl -L -O https://github.com/python-greenlet/greenlet/archive/0.4.0.tar.gz
tar xvzpf 0.4.0.tar.gz
cd greenlet-0.4.0
sudo python setup.py install
```

安装 `gevent-1.0rc2`，在终端中输入以下命令：

```sh
curl -L -O https://github.com/downloads/surfly/gevent/gevent-1.0rc2.tar.gz
tar xvzpf gevent-1.0rc2.tar.gz
cd gevent-1.0rc2
sudo python setup.py install
```

继续在终端输入以下命令：

```sh
cd path（path 为 goagent 文件夹的绝对地址）
```

从而进入 `goagent` 目录，再次使用 `cd` 命令进入 `server` 目录，执行以下命令：

```sh
python uploader.zip
```

根据提示输入 appid（即刚才创建的应用名称）、Gmail 帐号、密码来上传服务端程序。上传完成后，使用 `cd` 命令进入 `goagent` 目录下的 `local` 目录，执行以下命令：

```sh
python proxy.py
```

到这里本步骤就完成了。

## 4. 安装 Proxy SwitchySharp 插件

在谷歌浏览器应用商店搜索 Proxy SwitchySharp 插件，并「添加到Chrome」。

进入「SwitchySharp 选项」，选择「导入／导出」选项卡，在「在线恢复备份」按钮后方文本框输入 `https://wwqgtxx-goagent.googlecode.com/files/SwitchyOptions.bak`，并点击「在线恢复备份」按钮，即可导入已经配置好的设置，完成后可以关闭该页面。

点击谷歌浏览器地址栏右边的 SwitchySharp 插件按钮，选择「自动切换模式」。

之后的操作对于 Windows 和 OS X 又有一些区别，我将再次分开介绍。

### Windows

只要保证已经运行 `goagent.exe` 程序，并且没有关闭，就可以使用谷歌浏览器访问在国内被限制的网站了（提示：可以将 `goagent.exe` 设置为开机启动，从而不用每次都手动去运行）。

### OS X

前往 [https://github.com/ohdarling/GoAgentX/releases](https://github.com/ohdarling/GoAgentX/releases) 下载最新版本的 GoAgentX 并安装。

安装完运行，在主窗口的「服务配置」选项卡中设置好 App ID，点击「状态」选项卡的「启动」按钮即可使用谷歌浏览器访问在国内被限制的网站了（提示：可以在「其他设置」选项卡勾选「在用户登录时自动启动 GoAgentX」 ，从而不用每次都手动去运行）。
