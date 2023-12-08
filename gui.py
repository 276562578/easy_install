import tkinter as tk

import tools


class BasePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Easy Install")
        self.geometry("400x400")
        # self.resizable(False, False)
        self.minsize(800, 300)

class MainPage(BasePage):
    def __init__(self):
        super().__init__()
        # self.resizable(False, False)
        self.main_page()
        self.config=tools.Config()
        self.apps=self.config.get_apps()

    def main_page(self):
        self.frame_main = tk.Frame(self)
        self.frame_main.pack(fill=tk.BOTH, expand=tk.YES)

        # 创建按钮的容器Frame，并设置为可以在横向和纵向上扩展
        self.frame_buttons = tk.Frame(self.frame_main)
        self.frame_buttons.pack(fill=tk.BOTH, expand=tk.YES, padx=10, pady=10)

        # 创建按钮
        button1 = tk.Button(self.frame_buttons, text="超级菜鸟", command=self.click_button1)
        button2 = tk.Button(self.frame_buttons, text="中级选手", command=self.click_button2)
        button3 = tk.Button(self.frame_buttons, text="高级选手", command=self.click_button3)
        button4 = tk.Button(self.frame_buttons, text="顶级大佬", command=self.click_button4)

        # 使用Grid布局管理器布局按钮，并设置为填充整个网格单元格
        button1.grid(row=0, column=0, sticky="nsew", padx=10, pady=50)
        button2.grid(row=0, column=1, sticky="nsew", padx=10, pady=50)
        button3.grid(row=0, column=2, sticky="nsew", padx=10, pady=50)
        button4.grid(row=0, column=3, sticky="nsew", padx=10, pady=50)

        # 配置按钮容器Frame的每列的权重，以确保按钮横向平均分布并填充整个空间
        for i in range(4):
            self.frame_buttons.grid_columnconfigure(i, weight=1)

        # 配置按钮容器Frame的行权重，以确保按钮在垂直方向上居中
        self.frame_buttons.grid_rowconfigure(0, weight=1)



    def click_button1(self):
        self.frame_main.pack_forget()
        self.role1_page()
    def click_button2(self):
        self.frame_main.pack_forget()
        self.role2_page()
    def click_button3(self):
        self.frame_main.pack_forget()
        self.role3_page()
    def click_button4(self):
        self.frame_main.pack_forget()
        self.role4_page()

    def role1_page(self):
        # 当前页面背景框架
        self.frame_role1 = tk.Frame(self)
        self.frame_role1.pack(fill=tk.BOTH, expand=tk.YES)

        # 第一行frame
        self.frame_role1_sub1 = tk.Frame(self.frame_role1)
        self.frame_role1_sub1.pack()
        label = tk.Label(self.frame_role1_sub1, text="选择你想安装的软件或者进行搜索")
        label.grid(row=0, column=0, padx=10, pady=10)
        searcher = tk.Entry(self.frame_role1_sub1)
        searcher.grid(row=0, column=1, padx=10, pady=10)

        # 第二行frame
        self.frame_role1_sub2 = tk.Frame(self.frame_role1)
        self.frame_role1_sub2.pack(fill=tk.BOTH, expand=tk.YES)
        # 构建应用列表
        for i,app_name in enumerate(self.apps):
            # 组合成一个
            app=tk.Frame(self.frame_role1_sub2)
            app.grid(row=i//4,column=i%4,padx=10,pady=10)
            # 组成元素
            app_icon=tk.Label(app,text="图标")
            app_icon.pack(side="top")
            app_select=tk.Checkbutton(app)
            app_select.pack(side="left")
            app_name=tk.Label(app,text=app_name)
            app_name.pack(side="left")


        # 第三行的确认frame
        self.frame_role1_sub3=tk.Frame(self.frame_role1,class_="role1_sub3")
        self.frame_role1_sub3.pack(side="bottom",fill=tk.X,padx=10,pady=10)
        button_confirm=tk.Button(self.frame_role1_sub3,text="确认")
        button_confirm.pack(side="right",padx=10,pady=10)


    def role2_page(self):
        pass
    def role3_page(self):
        pass
    def role4_page(self):
        pass





if __name__ == "__main__":
    app = MainPage()
    app.mainloop()