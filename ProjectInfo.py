class ProjectInfo:
    name = ""
    local_path = ""
    remote_path = ""

    def __init__(self, name, local_path, remote_path):
        self.name = name
        self.local_path = local_path
        self.remote_path = remote_path
