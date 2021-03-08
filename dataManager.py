#  Copyright (c) 2021. Ivan Zinin

import os

import jsonpickle

from SettingsInfo import SettingsInfo

SETTINGS_FILE = 'usr/settings.json'
PROJECTS_FILE = 'usr/projects.json'
REMOTES_FILE = 'usr/remotes.json'

LOCAL_PATH = 'local_path'
REMOTE_PATH = 'remote_path'


#
######## Settings ########
#


def load_settings():
    try:
        settings_info = load_from_file(SETTINGS_FILE).get(SettingsInfo.DEFAULT)
    except FileNotFoundError:
        settings_info = SettingsInfo(os.getcwd())
        save_settings(settings_info)
        return settings_info
    if not settings_info:
        settings_info = SettingsInfo(os.getcwd())
        save_settings(settings_info)
    return settings_info


def save_settings(settings_info):
    save_to_file(SETTINGS_FILE, SettingsInfo.DEFAULT, settings_info)


def clear_settings():
    clear_file(SETTINGS_FILE)
    print('Cleared settings')


#
######## Remotes ########
#


def load_remotes():
    return load_from_file(REMOTES_FILE)


def save_remote(remote_info):
    save_to_file(REMOTES_FILE, remote_info.name, remote_info)
    print(f'Saved remote: \'{remote_info.name}\'')


def delete_remote(remote_name):
    delete_from_file(REMOTES_FILE, remote_name)
    print(f'Deleted remote: \'{remote_name}\'')


def delete_all_remotes():
    clear_file(REMOTES_FILE)
    print('Deleted all remotes')


#
######## Projects ########
#


def load_projects():
    return load_from_file(PROJECTS_FILE)


def save_project(project_info):
    save_to_file(PROJECTS_FILE, project_info.name, project_info)
    print(f'Saved project: \'{project_info.name}\'')


def delete_project(project_name):
    delete_from_file(PROJECTS_FILE, project_name)
    print(f'Deleted project: \'{project_name}\'')


def delete_all_projects():
    clear_file(PROJECTS_FILE)
    print('Deleted all projects')


#
######## Generic file IO ########
#


def save_to_file(file_name, key, value):
    try:
        with open(file_name, 'r') as f:
            data = jsonpickle.decode(f.read())
    except FileNotFoundError:
        data = {}
        pass
    data[key] = value
    with open(file_name, 'w') as f:
        f.write(jsonpickle.encode(data))


def load_from_file(file_name):
    with open(file_name, 'r') as f:
        data = jsonpickle.decode(f.read())
    return data


def clear_file(file_name):
    with open(file_name, 'w') as f:
        data = {}
        f.write(jsonpickle.encode(data))


def delete_from_file(file_name, key):
    try:
        with open(file_name, 'r') as f:
            data = jsonpickle.decode(f.read())
    except FileNotFoundError:
        print('Nothing to delete!')
        return
    with open(file_name, 'w') as f:
        item_to_delete = data.get(key)
        if not item_to_delete:
            return
        data.pop(key)
        f.write(jsonpickle.encode(data))
