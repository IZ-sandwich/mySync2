# mySync2
Another attempt now with python at ninja copy

## Args:
```
usage: mySync2.py [-h] [-c PROJECT_NAME] [-d PROJECT_NAME] [-l] [--deleteall]
                  [-cr ENDPOINT_NAME] [-dr ENDPOINT_NAME] [-lr] [--runtests]

  -h, --help            show this help message and exit
  -c PROJECT_NAME, --create PROJECT_NAME
                        Create new project with specified name
  -d PROJECT_NAME, --delete PROJECT_NAME
                        Delete an existing project with specified name
  -l, --list            List existing projects
  --deleteall           Delete ALL existing projects
  -cr ENDPOINT_NAME, --createremote ENDPOINT_NAME
                        Create new project with specified name
  -dr ENDPOINT_NAME, --deleteremote ENDPOINT_NAME
                        Delete an existing project with specified name
  -lr, --listremotes    List existing remote endpoints
  --runtests            run tests
```

## Setup instructions:
### Python packages
```
pip3 install jsonpickle
```

### Other stuff
Make sure to set up ssh keys:
On local machine: ```ssh-keygen``` 
On remote machine: ```ssh-copy-id username@address```

For debian:
- rsync: ```apt-get install rsync```
- inotifywait: ```apt-get install inotify-tools```
