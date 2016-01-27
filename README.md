# QQmail_Attach_Download
Download the attachments of QQ mailbox
##### Note
这个小脚本程序可以用来从QQ邮箱中批量下载附件。
批量下载附件QQ邮箱本身是提供的，但是却无法使用（不知道是我电脑自身原因还是什么）。

使用Python requests包实现文件下载。
没有模拟登录过程（邮箱的模拟登录我没弄好），所以只能在浏览器上登录，然后获取你自己的cookie,
以字典的形式作为参数传入。
