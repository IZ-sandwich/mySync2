#  Copyright (c) 2021. Ivan Zinin


class RemoteInfo:
    name = ""
    username = ""
    address = ""
    last_used_remote_path = ''

    DEFAULT_REMOTE_PATH = '/home/pi/workspace'
    REMOTE_PATH = 'remote_path'

    def __init__(self, name, username, address):
        self.name = name
        self.username = username
        self.address = address
