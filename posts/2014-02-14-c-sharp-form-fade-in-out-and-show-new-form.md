title: C# WinForm 程序窗体淡入淡出效果以及显示第二个窗体

前几天开始学 C#，到目前遇到了不少问题，也大都最终解决，下面来分享两个。

## 窗体淡入淡出效果

很多软件启动时会以淡入的形式出现，显得不那么突兀，那么是如何做到的？其实很简单，只需要用一个 `Timer` 来处理即可。这里简洁起见，只讲在窗体第一次启动时淡入。

首先在设计视图拖入一个 `Timer` 控件，属性先保持默认，然后在代码视图加入下面两个方法（当然你也可以在属性面板双击相应事件自动跳转到代码视图）：

```csharp
private void Form1_Load(object sender, EventArgs e)
{
	this.Opacity = 0.0;
	timer1.enable = true;
}

private void timer1_Tick(object sender, EventArgs e)
{
	if (this.Opacity < 1.0)
		this.Opacity += 0.2;
	else
		timer1.enable = false;
}
```

然后把这两个方法连接到分别连接到 `Form1` 的 `Load` 事件和 `timer1` 的 `Tick` 事件即可。

启动程序这时候窗体就是淡入的了。但是你可能会觉得淡入的速度非常慢，这时候要调整 `Timer` 的时间间隔即 `Interval`，默认是 100 毫秒，也就是说每 100 毫秒执行一次 `timer1_Tick` 方法，尝试改小一点，可以加快淡入的速度。

## 显示第二个窗体

首先得创建第二个窗体，才能显示。右击解决方案资源管理器中的项目名称，依次选择「添加」－「Windows 窗体」，命名（这里命名为 `Form2`）后点击「添加」之后，便创建了一个新的窗体，从代码上看上是创建了一个继承自 `Form` 类的一个新类。这时候要想通过在第一个窗体中点击按钮来显示新窗体，怎么做？

首先拖一个 `Button` 到原先的窗体，双击这个 `Button`，进入代码视图，在 `Button_Click` 方法中添加下面代码：

```csharp
private void button1_Click(object sender, EventArgs e)
{
	Form2 newForm = new Form2();
	newForm.Show();
}
```

运行程序，点击按钮，即可显示新窗体。
