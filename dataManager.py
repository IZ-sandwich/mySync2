import jsonpickle

SETTINGS_FILE = 'settings.json'
PROJECTS_FILE = 'projects.json'
DEFAULT_LOCAL_PATH = '/mnt/c/Users/Ivan/workspace'
DEFAULT_REMOTE_PATH = '/home/pi/workspace'
last_used_local_path = ''
last_used_remote_path = ''

LOCAL_PATH = 'local_path'
REMOTE_PATH = 'remote_path'


def load_settings():
    with open(SETTINGS_FILE, 'r') as f:
        data = jsonpickle.decode(f.read())
        print('data loaded: ')
        print(data)


def save_settings():
    with open(SETTINGS_FILE, 'w') as f:
        data = {LOCAL_PATH: DEFAULT_LOCAL_PATH,
                REMOTE_PATH: DEFAULT_REMOTE_PATH}
        if last_used_local_path != '':
            data = data[LOCAL_PATH] = last_used_local_path
        if last_used_remote_path != '':
            data = data[REMOTE_PATH] = last_used_remote_path
        f.write(jsonpickle.encode(data))


def save_project(project_info):
    with open(PROJECTS_FILE, 'r') as f:
        data = jsonpickle.decode(f.read())
    data[project_info.name] = project_info
    with open(PROJECTS_FILE, 'w') as f:
        f.write(jsonpickle.encode(data))


def delete_project(project_name):
    with open(PROJECTS_FILE, 'r') as f:
        data = jsonpickle.decode(f.read())
    with open(PROJECTS_FILE, 'w') as f:
        project = data.pop(project_name)
        f.write(jsonpickle.encode(data))
    print('deleted project: ')
    print(project.name)
    print('\n')


def delete_all_projects():
    with open(PROJECTS_FILE, 'w') as f:
        data = {}
        f.write(jsonpickle.encode(data))


def load_projects():
    with open(PROJECTS_FILE, 'r') as f:
        data = jsonpickle.decode(f.read())
    return data
