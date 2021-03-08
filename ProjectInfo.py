#  Copyright (c) 2021. Ivan Zinin


class ProjectInfo:
    name = ""
    local_path = ""
    remote_path = ""
    remote_name = ""

    def __init__(self, name, local_path, remote_path, remote_name):
        self.name = name
        self.local_path = local_path
        self.remote_path = remote_path
        self.remote_name = remote_name
