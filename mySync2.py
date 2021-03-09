#!/usr/bin/python3

#  Copyright (c) 2021. Ivan Zinin

# This is another attempt at the ninja copy script.
# This time my requirements are to save the project paths and names in a file, as well as remote endpoints, and any
# other local settings.

import argparse

import dataManager
import syncManager
from SyncThread import SyncThread
from tests import run_tests
from utils import print_remotes, print_projects, get_new_project_info, get_new_remote_info


def main():
    dataManager.load_settings()

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", type=str, metavar='PROJECT_NAME',
                        help="Create new project with specified name")
    parser.add_argument("-d", "--delete", type=str, metavar='PROJECT_NAME',
                        help="Delete an existing project with specified name")
    parser.add_argument("-l", "--list", action="store_true", help="List existing projects")
    parser.add_argument("--deleteall", action="store_true", help="Delete ALL existing projects")
    parser.add_argument("-cr", "--createremote", type=str, metavar='ENDPOINT_NAME',
                        help="Create new project with specified name")
    parser.add_argument("-dr", "--deleteremote", type=str, metavar='ENDPOINT_NAME',
                        help="Delete an existing project with specified name")
    parser.add_argument("-lr", "--listremotes", action="store_true", help="List existing remote endpoints")
    parser.add_argument("--runtests", action="store_true", help="run tests")
    args = parser.parse_args()
    if args.create:
        dataManager.load_projects().get(args.create)
        print(f'Creating a new project \'{args.create}\'')
        new_project = get_new_project_info(args.create)
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
        in_str = input('Are you sure you want to delete ALL projects? (Y/N):')
        if in_str == 'Y':
            dataManager.delete_all_projects()
        else:
            print('Cancelling\n')
            exit(0)
    elif args.createremote:
        print(f'Creating a new remote endpoint \'{args.createremote}\'\n')
        new_remote = get_new_remote_info(args.createremote)
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
