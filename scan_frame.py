import tkinter as tk
import json

# 创建一个Tkinter窗口
root = tk.Tk()

# 隐藏窗口标题栏和边框
root.overrideredirect(True)

# 将窗口置顶
root.wm_attributes("-topmost", True)

# 设置窗口大小和位置
with open('region.txt', 'r', encoding='u8') as f:
    region = tuple(json.load(f))
root.geometry(f'{region[2]}x{region[3]}+{region[0]//2-region[2]//2}+{region[1]//2-region[3]//2}')

# 将窗口背景设为透明
root.attributes('-transparentcolor', 'white')

# 将窗口的画布设为透明
canvas = tk.Canvas(root, bg='white', highlightthickness=0)
canvas.pack(fill='both', expand=True)

# 绘制一个红色空心正方形
canvas.create_rectangle(5, 5, region[2]-5, region[3]-5, outline='red', width=3)

# 进入循环让窗口保持打开状态
root.mainloop()