title: UITextField 点击 Return 后隐藏键盘
categories: Tech
tags: [iOS, Objective-C]

关于这个问题，当初到处查，现在看来，已经是个很简单的问题了，不过还是记一下吧。

首先把 `UITextField` 的 `delegate` 设置成当前的 `ViewController`，然后在 `ViewController.m` 里的 `@implementation` 的任意处添加下面一个代理方法：

```objc
- (BOOL)textFieldShouldReturn:(UITextField *)textField
{

}
```

然后就是在这个方法里面添加代码了，比如：

```objc
- (BOOL)textFieldShouldReturn:(UITextField *)textField
{
        [textField resignFirstResponder];
        return YES;
}
```

当然这方法里你想干嘛都行，比如检查输入是否符合格式、调用登录方法等等。如果有多个文本框需要输入，希望点 Return 跳到下一个，就给下一个文本框的 `outlet` 发送 `becomeFirstResponder` 消息即可。

如果你要做类似于登录的东西，要既可以点按钮登录，也可以在最后一个文本框点 Return 登录的话，可以加上下面这行代码：

```objc
if (textField == lastTextField)
        [loginBtn sendActionsForControlEvents:UIControlEventTouchUpInside];
```

这条消息模拟点击了 `loginBtn`。

有一个要注意的就是，把多个 `UITextField` 的 `delegate` 设置到一个类的话，他们是共用一套代理方法，你需要在代理方法里面去判断是哪个文本框。
