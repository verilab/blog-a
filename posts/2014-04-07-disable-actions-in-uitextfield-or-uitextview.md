title: Disable actions in UITextField or UITextView
categories: Tech
tags: [iOS, Objective-C]

In many cases, we need to disable some actions in `UITextField` or `UITextView` so that users cannot edit the texts. I have two methods here.

## Method 1

A simple but fast way to achieve the goal is to stop the textview or textfield from becoming first responder.

Simply make the `Enabled` or `User Interaction Context` attributes unchecked in `Interface Builder`. The effects of unchecking these two attributes are not exactly the same, and it is easy to find the difference.

If you will, you can add the following line in code instead of do it in IB:

```objc
textField.userInteractionEnabled = NO;
```

## Method 2

This method is to stop specific actions like `copy`, `cut`, `paste`.

Create a subclass of `UITextField` or `UITextView`, and override the `canPerformAction:withSender:` method like following:

```objc
- (BOOL)canPerformAction:(SEL)action withSender:(id)sender
{
    if (action == @selector(copy:))
        return NO;
    return [super canPerformAction:action withSender:sender];
}
```
