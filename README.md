# Genshin-QR
原神直播抢码工具，识别屏幕上的二维码

## 使用方法
1. 打开命令提示符（Win+R输入cmd回车），并将目录切换至项目文件夹下`cd [你的电脑保存本项目的文件夹路径]`
2. 检查是否安装Python并配置好环境变量`python -V 和 pip -V`，返回版本号则表示成功
3. 安装项目所需依赖包`pip install -r requirements.txt`
4. 运行程序`python Genshin_login_tool_cv2.py`

## 如果要打包成exe使用
1. 最好用集成开发工具（如Pycharm）打开本项目
2. 上述第3步在集成开发工具的“终端”选项卡中操作，使依赖包安装在项目虚拟环境（venv）中
3. 在“终端”选项卡中安装pyinstaller，`pip install pyinstaller`
4. 在“终端”选项卡中运行打包命令：`pyinstaller -F ./Genshin_login_tool_cv2.py`，即可在生成的`dist`目录下得到对应的exe文件

## 米游社cookie的获取方式（以Chrome浏览器为例）
1. 打开浏览器，进入无痕浏览模式
2. 访问[https://user.mihoyo.com/](https://user.mihoyo.com/)，登录
3. 打开开发者模式（快捷键F12），点击`控制台/Console`选项卡
4. 输入`document.cookie`回车，鼠标光标放到返回的内容上，右键->点“复制字符串内容”

   示例图（因为我没有登录，所以返回的内容很短）：
   ![image](https://github.com/Mr-Deng67/Genshin-QR/assets/52495231/9f7479e2-0c6d-4ac1-81c0-f42db187fdb0)

## 参考与感谢
[wintersnowlc/Genshin_login_tool](https://github.com/wintersnowlc/Genshin_login_tool)
