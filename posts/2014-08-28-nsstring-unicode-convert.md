title: 将 NSString 字符串转换成 Unicode 编码

今天是突然想把一些字符串转成形如 `\u597d` 的 Unicode 编码。

> 统一码的编码方式与 ISO 10646 的通用字符集概念相对应。目前实际应用的统一码版本对应于 UCS-2，使用 16 位的编码空间。也就是每个字符占用 2 个字节。这样理论上一共最多可以表示 216（即65536）个字符。基本满足各种语言的使用。实际上当前版本的统一码并未完全使用这 16 位编码，而是保留了大量空间以作为特殊使用或将来扩展。 ------维基百科「Unicode」词条

于是写了两个类方法，如下：

```objc
+ (NSString *)unicodeStringWithString:(NSString *)string {
    NSString *result = [NSString string];
    for (int i = 0; i < [string length]; i++) {
        result = [result stringByAppendingFormat:@"\\u%04x", [string characterAtIndex:i]];
        /*
         因为 Unicode 用 16 个二进制位（即 4 个十六进制位）表示字符，对于小于 0x1000 字符要用 0 填充空位，
         所以使用 %04x 这个转换符，使得输出的十六进制占4位并用0来填充开头的空位。
         */
    }
    return result;
}

+ (NSString *)stringWithUnicodeString:(NSString *)string {
    NSArray *strArray = [[string substringFromIndex:2] componentsSeparatedByString:@"\\u"];
    NSString *result = [NSString string];
    for (NSString *str in strArray) {
        NSString *tmpStr = [@"0x" stringByAppendingString:str];
        unichar c = strtoul([tmpStr UTF8String], 0, 0);
        /*
         上面两行也可以写成下面一行：
         unichar c = strtoul([str UTF8String], 0, 16);
         */
        result = [result stringByAppendingString:[NSString stringWithCharacters:&c length:1]];
    }
    return result;
}
```
