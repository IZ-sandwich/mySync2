#  Copyright (c) 2021. Ivan Zinin
import dataManager
from ProjectInfo import ProjectInfo
from RemoteInfo import RemoteInfo


def print_projects(projects):
    print('Printing projects:')
    for name in projects:
        print(f'project name: {name}')
        print(f'  local path: {projects[name].local_path}')
        print(f'  remote path: {projects[name].remote_path}')
        print(f'  remote endpoint name: {projects[name].remote_name}')
        print('\n')


def print_remotes(remotes):
    print('Printing remote endpoints:')
    for name in remotes:
        print(f'remote endpoint name: {name}')
        print(f'  username: {remotes[name].username}')
        print(f'  address: {remotes[name].address}')
        print(f'  last used remote path: {remotes[name].last_used_remote_path}')
        print('\n')


def get_new_remote_info(new_remote_name):
    address = input('Enter address for new remote connection:')
    username = input('Enter username for new remote connection:')
    return RemoteInfo(new_remote_name, username, address)


def get_new_project_info(new_project_name):
    settings = dataManager.load_settings()
    remotes = dataManager.load_remotes()
    print_remotes(remotes)
    remote_name = input('Enter remote name to use:')
    remote_for_new_project = remotes.get(remote_name)
    if not remote_for_new_project:
        in_str = input(f'Remote with name \'{remote_name}\' does not exist,'
                       f' would you like to create a new one? (Y/N):')
        if in_str == 'Y':
            remote_for_new_project = get_new_remote_info(remote_name)
        else:
            print('Cancelling\n')
            exit(0)

    suggested_local_path = settings.last_used_local_path + '/' + new_project_name
    new_local_path = input(f'Enter local project path or use empty for \'{suggested_local_path}\':')
    if new_local_path == '':
        new_local_path = suggested_local_path

    suggested_remote_path = remote_for_new_project.last_used_remote_path + '/' + new_project_name
    new_remote_path = input(f'Enter remote project path or use empty for \'{suggested_remote_path}\':')
    if new_remote_path == '':
        new_remote_path = suggested_remote_path

    # Update last used paths
    settings.last_used_local_path = new_local_path[:new_local_path.rfind('/')]
    dataManager.save_settings(settings)
    remote_for_new_project.last_used_remote_path = new_remote_path[:new_remote_path.rfind('/')]
    dataManager.save_remote(remote_for_new_project)

    return ProjectInfo(new_project_name, new_local_path, new_remote_path, remote_for_new_project.name)
