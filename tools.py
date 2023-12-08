# 解析yml文件
import logging
import os

import yaml

class Config:
    def __init__(self):
        self.config_dir="config"

    def get_config(self,app=None,os=None):
        config_file=os.path.join(self.config_dir,app,f"{os}.yml")
        with open(config_file,encoding="utf-8") as f:
            config=yaml.safe_load(f)
        return config

    def get_apps(self):
        return [app for app in os.listdir(self.config_dir)]