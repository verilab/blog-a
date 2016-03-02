title: C# 检测是否有网络连接
categories: Tech
tags: [C#, Windows, dotNET]

最近在做的一个项目需要在后台不断检测是否有网络连接，一开始用 `Ping` 来检测，代码如下：

```csharp
using System.Text;
using System.Net.NetworkInformation;

private bool hasInternetAccess()
{
	try
	{
		Ping ping = new Ping();
		PingOptions options = new PingOptions();
		options.DontFragment = true;
		string data = "";
		byte[] buffer = Encoding.ASCII.GetBytes(data);
		int timeout = 1000;
		PingReply reply = ping.Send("114so.cn", timeout, buffer, options);
		if (reply.Status == IPStatus.Success)
			return true;
		else
			return false;
	}
	catch ()
	{
		return false;
	}
}
```

但是后来发现 ping 了几次后就会莫名其妙的 ping 不通（明明网络是通畅的），不管把 `timeout` 设置成多大都会出现这个情况。后来查了一下，找到另一种方法，是通过调用 API 函数来实现的，代码如下：

```csharp
using System.Runtime;
using System.Runtime.InteropServices;

[DllImport("wininet.dll")]
private extern static bool InternetGetConnectedState(int Description, int ReservedValue);

private bool hasInternetAccess()
{
	return InternetGetConnectedState(0, 0);
}
```

用这个方法之后，就没有出现明明网络通畅却返回 false 的情况了。
