# Genshin-Code-Scanner
原神直播抢码工具，识别屏幕上的二维码

## 使用方法
- 使用Python运行
   1. 打开命令提示符（Win+R输入cmd回车），并将目录切换至项目文件夹下`cd [你的电脑保存本项目的文件夹路径]`
   2. 检查是否安装Python并配置好环境变量`python -V 和 pip -V`，返回版本号则表示成功
   3. 安装项目所需依赖包`pip install -r requirements.txt`
   4. 运行程序`python Genshin_login_tool.py`
- 直接下载[发行版](https://github.com/Mr-Deng67/Genshin-Code-Scanner/releases)

## region.txt说明
这个文件用来设置扫描范围  
**只有里面的四个数字可以修改，其他字符不要去动**  
四个数字的含义：预设的[1920, 1080, 250, 250]，即表示屏幕分辨率为1920x1080，扫描区域为以屏幕中心宽250高250的正方形区域

## 米游社cookie的获取方式（以Chrome浏览器为例）
1. 打开浏览器，进入无痕浏览模式
2. 访问[https://user.mihoyo.com/](https://user.mihoyo.com/)，登录
3. 打开开发者模式（快捷键F12），点击`控制台/Console`选项卡
4. 输入`document.cookie`回车，鼠标光标放到返回的内容上，右键->点“复制字符串内容”

   示例图（因为我没有登录，所以返回的内容很短）：
   ![image](https://github.com/Mr-Deng67/Genshin-QR/assets/52495231/9f7479e2-0c6d-4ac1-81c0-f42db187fdb0)

## 参考与感谢
[wintersnowlc/Genshin_login_tool](https://github.com/wintersnowlc/Genshin_login_tool)
