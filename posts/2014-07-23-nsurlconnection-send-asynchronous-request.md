title: NSURLConnection 发送异步请求

很简单，代码如下：

```objc
[NSURLConnection sendAsynchronousRequest:[NSURLRequest requestWithURL:[NSURL URLWithString:urlString]]
                                   queue:[[NSOperationQueue alloc] init]
                       completionHandler:^(NSURLResponse *response, NSData *data, NSError *connectionError) {
                               //异步请求完成后的操作
                       }];
```

这里的 `[NSURLRequest requestWithURL:[NSURL URLWithString:urlString]]` 创建了一个 URL 请求。`[[NSOperationQueue alloc] init]` 创建了一个新的操作队列，`NSOperationQueue` 用来管理其中的操作在一个或多个线程中执行，上面代码指定一个 `NSOperationQueue` 就是让请求在新的操作队列完成。`completionHandler:` 后面跟一个 Block 作参数，用来在请求完成后进行后续操作，比如检查返回的的数据以及更改界面等。

然而因为这个 Block 不是在主线程执行的，而更改界面的操作需要在主线程进行，所以如果要在 `completionHandler` 中更改界面，需要用以下代码：

```objc
[[NSOperationQueue mainQueue] addOperationWithBlock:^ {
        //更改界面的操作
}];
```

这样就可以实现异步请求了，比如下面这样：

```objc
[acticityIndicator startAnimating];
[NSURLConnection sendAsynchronousRequest:[NSURLRequest requestWithURL:[NSURL URLWithString:urlString]]
                                   queue:[[NSOperationQueue alloc] init]
                       completionHandler:^(NSURLResponse *response, NSData *data, NSError *connectionError) {
                               [[NSOperationQueue mainQueue] addOperationWithBlock:^ {
                                       [acticityIndicator stopAnimating];
                               }];
                               
                               if (connectionError == nil) {
                                       [data writeToFile:[NSTemporaryDirectory() stringByAppendingPathComponent:@"data.plist"]
                                              atomically:YES];
                               }
                       }];

```

Enjoy!
