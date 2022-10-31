import json
import os


class Setting:

    def __init__(self, json_file):

        self.setting_file = 'xiaoyuanwangsetting.json'
        self.setting_path = "" + self.setting_file
        self.setting_abs = None
        self.json_file = json_file
        self.setting_path = self.__get_setting_path()



    def __create_setting_json(self):
        with open(self.setting_path, 'w') as f:
            json.dump(self.json_file, f, indent=4)

    def __get_setting_path(self):

        """
        获取配置文件路径；

        :return:
        """

        # 先判断配置文件是否存在
        appdata_setting_path = os.path.join(os.getenv("APPDATA"), self.setting_file)
        if os.path.exists(self.setting_path):
            # 根目录存在
            self.setting_path = self.setting_file
            self.setting_abs = False
        else:
            """
            如果根目录没有配置配置文件，则将配置文件目录定位在用户AppData目录 
            """
            self.setting_path = appdata_setting_path
            self.setting_abs = True
            if not os.path.exists(appdata_setting_path):
                """
                如果这个文件不存在，则创建一个
                """
                self.__create_setting_json()

        return self.setting_path

    def read_setting_file(self):
        """
        根据配置文件路径 读取配置文件
        :return:
        """
        with open(self.setting_path, 'r') as f:
            json_file = json.load(f)
        return self.setting_abs, json_file

    def save_setting_file(self, json_file):
        """

        :param json_file: 新的配置文件
        :return:
        """
        print(json_file)
        with open(self.setting_path, 'w') as f:
            json.dump(json_file, f, indent=4)
