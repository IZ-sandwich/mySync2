# in bash the following code was used:
# for synching:
# rsync -av "$LOCAL_WORKSPACE/$1" "pi@$pi_address:$REMOTE_WORKSPACE/" --delete --exclude $RSYNC_IGNORES
#
# for waiting:
# error=`inotifywait $WAIT_ARGS "$LOCAL_WORKSPACE/$1" 1>/dev/null`

# Notes from previous attempt:
# exclude does not work cause need to exclude specific files, excluding events works i think*

import subprocess


def sync_project(project_info, remote_info):
    while True:
        print('Synchronizing ' + project_info.name)
        rsync_command = [f'rsync',
                         f'-av',
                         f'"{project_info.local_path}"',
                         f'"{remote_info.username}@{remote_info.address}:{project_info.remote_path}"',
                         f'--delete',
                         f'--exclude',
                         # rsync ignores:
                         f'"*.swp"']
        try:
            subprocess.run(rsync_command, check=True)
        except subprocess.CalledProcessError as e:
            print('Failed to sync with remote(rsync): ')
            print(e)
            raise e

        print('Waiting on updates in ' + project_info.name)
        inotifywait_command = [f'inotifywait',
                               # WAIT_ARGS
                               f'-r',
                               f'-e',
                               f'create',
                               f'-e',
                               f'delete',
                               f'-e',
                               f'modify',
                               f'-e',
                               f'moved_from',
                               f'-e',
                               f'moved_to',
                               f'--exclude',
                               # WAIT_IGNORES
                               f'".*\.swp"',
                               f'"{project_info.local_path}"',
                               f'1>/dev/null']
        try:
            subprocess.run(inotifywait_command, check=True)
        except subprocess.CalledProcessError as e:
            print('Failed to check local updates(inotifywait): ')
            print(e)
            raise e
