# This is another attempt at the ninja copy script.
# This time my requirements are to save the project paths and names in a file
# What I want to save:
# - local path
# - remote path
# - project name
# - default path values

import dataManager
from ProjectInfo import ProjectInfo


def test_settings():
    print('saving defaults')
    dataManager.save_settings()

    print('loading defaults')
    dataManager.load_settings()


def print_projects(projects):
    print('Printing projects:\n')
    for name in projects:
        print('project name: ' + name)
        print('local path: ' + projects[name].local_path)
        print('remote path: ' + projects[name].remote_path)
        print('\n')


def test_projects_load():
    print('deleting all projects\n')
    dataManager.delete_all_projects()
    print('saving project 1\n')
    project1 = ProjectInfo('project 1', '/derp/herp', '/pi/herp/derp')
    dataManager.save_project(project1)
    print('saving project two\n')
    project2 = ProjectInfo('project two', '/derp/herp/blah', '/pi/herp/derp/foodbar')
    dataManager.save_project(project2)
    print('loading back projects\n')
    projects = dataManager.load_projects()
    print_projects(projects)
    print('deleting project 1\n')
    dataManager.delete_project(project1.name)
    print('loading back projects\n')
    projects = dataManager.load_projects()
    print_projects(projects)

    print('\n')


if __name__ == '__main__':
    test_settings()
    test_projects_load()
