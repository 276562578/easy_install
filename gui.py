import logging
import os
import tkinter as tk
from PIL import Image, ImageTk
import tools

DEBUG = True
if DEBUG:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        self.apps=self.config.get_fine_apps()
        self.env=tools.Env()
        self.executor=tools.Executor()

    def main_page(self):
        self.frame_main = tk.Frame()
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
        self.frame_role1 = tk.Frame()
        self.frame_role1.pack(fill=tk.BOTH, expand=tk.YES)

        # 第一行frame
        self.frame_role1_sub1 = tk.Frame(self.frame_role1)
        self.frame_role1_sub1.pack()
        label = tk.Label(self.frame_role1_sub1, text="搜索：")
        label.grid(row=0, column=0, padx=10, pady=10)
        searcher = tk.Entry(self.frame_role1_sub1)
        searcher.grid(row=0, column=1, padx=10, pady=10)

        # 第二行frame
        # https://www.youtube.com/watch?v=0WafQCaok6g
        self.frame_role1_sub2 = tk.Frame(self.frame_role1)
        self.frame_role1_sub2.pack(fill=tk.BOTH, expand=tk.YES, padx=10, pady=10)
        canvas = tk.Canvas(self.frame_role1_sub2)
        canvas.pack(side="left", fill=tk.BOTH, expand=tk.YES)
        scrollbar = tk.Scrollbar(self.frame_role1_sub2,command=canvas.yview)  # https://blog.csdn.net/qq_28123095/article/details/79331756
        scrollbar.pack(side="left", fill=tk.Y, padx=10, pady=10)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        frame_app_list= tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_app_list, anchor='nw')
        # canvas内部的frame不能pack
        # frame_app_list.pack(fill=tk.BOTH, expand=tk.YES, padx=10, pady=10)
        scrollbar.config(command=canvas.yview)
        # 对于canvas内部不能太复杂，以下无效
        # for column in range(4): # 修改权重让格子一样大
        #     frame_app_list.grid_columnconfigure(column, weight=1)
        # for row in range(4):
        #     frame_app_list.grid_rowconfigure(row, weight=1)
        # 构建应用列表
        for i,app_name in enumerate(self.apps):
            # 定义变量
            app_name=app_name
            logging.debug(f"app_name:{app_name}")
            app_icon=os.path.join("config",app_name,"icon.png")
            app_config=self.config.get_config(app_name,"linux")["default"]
            if "desc" not in app_config.keys():
                app_config["desc"]="缺少描述"
            app_desc=app_config["desc"]
            app_default_run=app_config["default_run"]
            app_run=app_config["role1"]
            # 定义单个app的frame
            app=tk.Frame(frame_app_list)
            # app.grid(row=i//4,column=i%4,padx=10,pady=10,sticky='nsew')
            app.pack(fill=tk.X,expand=tk.YES,padx=10,pady=10)
            # 组成元素
            app_install = tk.Button(app, text="安装")
            app_install.pack(side="left")
            if os.path.exists(app_icon):
                im = Image.open(app_icon)
                ph = ImageTk.PhotoImage(im.resize((50,50)))
                app_icon=tk.Label(app,image=ph)
                app_icon.image=ph
                app_icon.pack(side="left")
            else:
                app_icon=tk.Label(app,text="图标缺失")
                app_icon.pack(side="left")
            # app_select=tk.Checkbutton(app)
            # app_select.pack(side="left")
            app_name=tk.Label(app,text=app_name)
            app_name.pack(side="left")
            app_desc=tk.Label(app,text=app_desc)
            app_desc.pack(side="left",fill=tk.X,expand=tk.YES)
            line=tk.Frame(frame_app_list,height=1,bg="black")
            line.pack(fill=tk.X,expand=tk.YES,padx=10,pady=10)

        # 第三行的确认frame
        # self.frame_role1_sub3=tk.Frame(self.frame_role1,class_="role1_sub3")
        # self.frame_role1_sub3.pack(fill=tk.BOTH,expand=tk.YES,padx=10,pady=10)
        # button_confirm=tk.Button(self.frame_role1_sub3,text="确认")
        # button_confirm.pack(side="right",padx=10,pady=10)


    def role2_page(self):
        pass
    def role3_page(self):
        pass
    def role4_page(self):
        pass





if __name__ == "__main__":
    app = MainPage()
    app.mainloop()