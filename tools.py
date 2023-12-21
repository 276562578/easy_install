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

    def get_apps(self):
        return [app for app in os.listdir(self.config_dir)]

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
