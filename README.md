# Genshin-QR
原神直播抢码工具，识别屏幕上的二维码

**参考 [wintersnowlc/Genshin_login_tool](https://github.com/wintersnowlc/Genshin_login_tool) 的代码，并进行了一些改进：**
1. 使用了速度更快的截图库，从而提升了识别二维码的速度
2. OpenCV库传入了微信扫码团队开源的神经网络模型文件，使其能够识别直播画面缩小时的二维码
3. 将抢码逻辑由原代码的1万次for循环改为while True死循环，使得识别二维码的次数不受限制（适用于主播不断刷新二维码的情况）
4. 将延迟登录由原来的随机数延迟改为用户自定义延迟秒数，支持输入小数，如输入1.5表示抢码成功后等待1.5秒再确认登录
5. 确认登录这部分代码以创建新线程的方式执行，解决了由于用户设置的延迟登录秒数过久，而主播在不断刷新二维码，此时的程序在延迟登录而不去识别后续的二维码的问题



**PS：本程序还是在用很low的抢码方式，像之前小86搞的30抽挑战赛都是被很牛的科技扫上的，哪种程序我写不出来。如果有厉害的大佬或了解这方面的欢迎**![image](https://github.com/Mr-Deng67/Genshin-QR/assets/52495231/689c2323-3da3-453f-adf8-fb8eb2c7b68b)


