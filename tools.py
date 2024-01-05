# 解析yml文件
import logging
import os

import yaml

class Config:
    def __init__(self):
        self.config_dir="config"

    def get_config(self,app,OS):
        config_file=os.path.join(self.config_dir,app,f"{OS}.yml")
        with open(config_file,encoding="utf-8") as f:
            config=yaml.safe_load(f)
        return config

    def get_fine_apps(self):
        app_all_list=os.listdir(self.config_dir)
        # 1. 检查app的文件结构
        app_folder_list=self.check_folder_structure(app_all_list)
        # 2. 检查yml文件结构
        app_yml_list=self.check_ymls_structure(app_folder_list)
        return app_yml_list

    def check_folder_structure(self, folders):
        app_clean=[]
        for app in folders:
            # 1. 检查yml文件
            if not os.path.exists(os.path.join(app,"linux.yml")) \
                and not os.path.exists(os.path.join("mac.yml")) \
                and not os.path.exists(os.path.join("win.yml")):
                logging.warning(f"{app}缺少至少一个yml文件")
                continue
            # 2. 检查icon文件
            if not os.path.exists(os.path.join(app,"icon.png")):
                logging.warning(f"{app}缺少icon文件")
                continue

            app_clean.append(app)
        return app_clean

    def check_ymls_structure(self, ymls):
        linux_yml_structure_require=["desc","compatible","default_run","role1"]
        yml_clean = []
        for yml in ymls:
            yml_content = self.get_config(yml, "linux")
            # 1. 检查default是否存在
            if "default" not in yml_content.keys():
                logging.warning(f"{yml}缺少default配置")
                continue
            # 2. 检查default的映射是否存在
            if yml_content["default"] not in yml_content.keys():
                logging.warning(f"{yml}的default映射不存在")
                continue
            # 3. 检查该结构内部是否完整
            if not set(linux_yml_structure_require).issubset(set(yml_content.keys())):
                logging.warning(f"{yml}的结构不完整")
                continue
            yml_clean.append(yml)
        return yml_clean



class Env:
    def __init__(self):
        pass

    def get_env(self,para):
        pass

    def set_env(self,para,value):
        pass

class Executor:
    def __init__(self):
        pass

    def mac(self):
        pass

    def win(self):
        pass

    def linux(self):
        pass
