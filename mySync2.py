#!/usr/bin/python3

#  Copyright (c) 2021. Ivan Zinin

# This is another attempt at the ninja copy script.
# This time my requirements are to save the project paths and names in a file, as well as remote endpoints, and any
# other local settings.

import argparse

import dataManager
import syncManager
from ProjectInfo import ProjectInfo
from RemoteInfo import RemoteInfo
from SettingsInfo import SettingsInfo
from SyncThread import SyncThread


def test_settings():
    print('clearing settings')
    dataManager.clear_settings()

    print('loading settings')
    dataManager.load_settings()

    print('clearing settings')
    dataManager.clear_settings()

    print('saving settings')
    test_setting = SettingsInfo('/mnt/c/Users/Ivan/workspace')
    dataManager.save_settings(test_setting)

    print('loading settings')
    dataManager.load_settings()


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


def test_remotes_load():
    print('deleting all remotes\n')
    dataManager.delete_all_remotes()
    print('saving remote 1\n')
    remote1 = RemoteInfo('remote 1', 'debian', '192.168.1.107')
    dataManager.save_remote(remote1)
    print('saving remotes two\n')
    remote2 = RemoteInfo('remote two', 'pi', 'raspberrypi.local')
    dataManager.save_remote(remote2)
    print('loading back remotes\n')
    remotes = dataManager.load_remotes()
    print_remotes(remotes)
    print('deleting remote 1\n')
    dataManager.delete_remote(remote1.name)
    print('loading back projects\n')
    remotes = dataManager.load_remotes()
    print_remotes(remotes)
    print('deleting remote 2\n')
    dataManager.delete_remote(remote2.name)

    print('\n')


def test_projects_load():
    print('deleting all projects\n')
    dataManager.delete_all_projects()
    print('saving project 1\n')
    project1 = ProjectInfo('project 1', '/derp/herp', '/pi/herp/derp', 'remote 1')
    dataManager.save_project(project1)
    print('saving project two\n')
    project2 = ProjectInfo('project two', '/derp/herp/blah', '/pi/herp/derp/foodbar', 'remote two')
    dataManager.save_project(project2)
    print('loading back projects\n')
    projects = dataManager.load_projects()
    print_projects(projects)
    print('deleting project 1\n')
    dataManager.delete_project(project1.name)
    print('loading back projects\n')
    projects = dataManager.load_projects()
    print_projects(projects)
    print('deleting project two\n')
    dataManager.delete_project(project2.name)

    print('\n')


def run_tests():
    print('Running tests!\n')
    test_settings()
    test_remotes_load()
    test_projects_load()


def get_project_info(new_project_name):
    settings = dataManager.load_settings()
    remotes = dataManager.load_remotes()
    print_remotes(remotes)
    remote_name = input('Enter remote name to use:')
    remote_for_new_project = remotes.get(remote_name)
    if not remote_for_new_project:
        in_str = input(f'Remote with name \'{remote_name}\' does not exist,'
                       f' would you like to create a new one? (Y/N):')
        if in_str == 'Y':
            remote_for_new_project = get_remote_info(remote_name)
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


def get_remote_info(new_remote_name):
    address = input('Enter address for new remote connection:')
    username = input('Enter username for new remote connection:')
    return RemoteInfo(new_remote_name, username, address)


def main():
    dataManager.load_settings()

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", type=str, metavar='PROJECT_NAME',
                        help="Create new sync link with specified name")
    parser.add_argument("-d", "--delete", type=str, metavar='PROJECT_NAME',
                        help="Delete an existing sync link with specified name")
    parser.add_argument("-l", "--list", action="store_true", help="List existing sync links")
    parser.add_argument("--deleteall", action="store_true", help="Delete ALL existing sync links")
    parser.add_argument("-cr", "--createremote", type=str, metavar='ENDPOINT_NAME',
                        help="Create new sync link with specified name")
    parser.add_argument("-dr", "--deleteremote", type=str, metavar='ENDPOINT_NAME',
                        help="Delete an existing sync link with specified name")
    parser.add_argument("-lr", "--listremotes", action="store_true", help="List existing remote endpoints")
    parser.add_argument("--runtests", action="store_true", help="run tests")
    args = parser.parse_args()
    if args.create:
        dataManager.load_projects().get(args.create)
        print(f'Creating a new project \'{args.create}\'')
        new_project = get_project_info(args.create)
        dataManager.save_project(new_project)
        remote_endpoint = dataManager.load_remotes().get(new_project.remote_name)
        try:
            syncManager.sync_project_once(new_project, remote_endpoint)
        except Exception as e:
            print('Failed to create new project!')
            print(e)
            dataManager.delete_project(new_project.name)
    elif args.delete:
        projects = dataManager.load_projects()
        project_to_delete = projects.get(args.delete)
        if project_to_delete:
            dataManager.delete_project(args.delete)
        else:
            print(f'Project with name \'{args.delete}\' does not exist')
    elif args.list:
        projects = dataManager.load_projects()
        print_projects(projects)
    elif args.deleteall:
        in_str = input('Are you sure you want to delete ALL sync links? (Y/N):')
        if in_str == 'Y':
            dataManager.delete_all_projects()
        else:
            print('Cancelling\n')
            exit(0)
    elif args.createremote:
        print(f'Creating a new remote endpoint \'{args.createremote}\'\n')
        new_remote = get_remote_info(args.createremote)
        dataManager.save_remote(new_remote)
        pass
    elif args.deleteremote:
        remotes = dataManager.load_remotes()
        remote_to_delete = remotes[args.deleteremote]
        if remote_to_delete:
            dataManager.delete_project(args.deleteremote)
            print(f'Deleted remote endpoint \'{args.deleteremote}\'\n')
        else:
            print(f'Remote endpoint with name \'{args.deleteremote}\' does not exist')
    elif args.listremotes:
        remotes = dataManager.load_remotes()
        print_remotes(remotes)
    elif args.runtests:
        # Run tests
        run_tests()
    else:
        print('Loading projects:')
        projects = dataManager.load_projects()
        remotes = dataManager.load_remotes()
        print_projects(projects)
        print('Starting sync\n')
        threads = []
        for project in projects:
            remote = remotes.get(projects.get(project).remote_name)
            threads.append(SyncThread(projects.get(project), remote))
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
        print('Done!\n')


if __name__ == '__main__':
    main()
