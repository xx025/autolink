import os


def remove_shortcut(shortcut_path: str):
    path = shortcut_path + '.lnk'

    if os.path.exists(path):  # 如果文件存在
        # 删除文件，可使用以下两种方法。
        os.remove(path)
        # os.unlink(path)
        return True

    else:
        return False
