#  Copyright (c) 2021. Ivan Zinin


class SettingsInfo:
    DEFAULT = 'DEFAULT'
    DEFAULT_LOCAL_PATH = '/mnt/c/Users/Ivan/workspace'

    last_used_local_path = ""

    def __init__(self, last_used_local_path):
        self.last_used_local_path = last_used_local_path
