#  Copyright (c) 2021. Ivan Zinin

import threading

from syncManager import sync_project


class SyncThread(threading.Thread):
    project_info = "not set"
    remote_info = "not set"

    def __init__(self, project_info, remote_info):
        threading.Thread.__init__(self)
        self.project_info = project_info
        self.remote_info = remote_info

    def run(self):
        print(f'starting {self.project_info.name}\n')
        sync_project(self.project_info, self.remote_info)
        print(f'exiting {self.project_info.name}\n')
