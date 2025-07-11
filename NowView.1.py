import time
import tkinter as tk
from tkinter import filedialog
import os

class FileMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件实时监控器")

        # 创建 Text 和 Scrollbar
        self.text = tk.Text(root, wrap="none", font=("Courier", 10), undo=True)
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)

        # 布局
        self.scrollbar.pack(side="right", fill="y")
        self.text.pack(side="left", expand=True, fill="both")

        # 文件选择
        self.file_path = filedialog.askopenfilename(title="请选择要监控的文件")
        if not self.file_path:
            print("未选择文件，退出。")
            root.destroy()
            return

        self.last_mtime = 0
        self.poll_interval = 1000  # 毫秒

        self.update_file_content()

    def update_file_content(self):
        try:
            mtime = os.path.getmtime(self.file_path)
            if mtime != self.last_mtime:
                self.last_mtime = mtime

            # ✅ 记录当前滚动条位置
            yview_pos = self.text.yview()

            # 读取文件内容
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # 更新内容
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, content)

            # ✅ 恢复滚动条位置
            self.text.yview_moveto(yview_pos[0])

        except Exception as e:
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, f"读取文件出错: {e}")

        # ✅ 调整下一次刷新时间
        self.root.after(self.poll_interval, self.update_file_content)


if __name__ == "__main__":
    root = tk.Tk()
    app = FileMonitorApp(root)
    root.mainloop()
