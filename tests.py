#  Copyright (c) 2021. Ivan Zinin
import dataManager
from ProjectInfo import ProjectInfo
from RemoteInfo import RemoteInfo
from SettingsInfo import SettingsInfo
from utils import print_remotes, print_projects


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
