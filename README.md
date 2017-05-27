# Smart RM

Using linux "rm" interface let remove to trash and restore from it.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing

##### Step 1. Download from git
Create a local clone of your project

```
$ git clone https://kat6123@bitbucket.org/kat6123/labs.git <folder_name>
```

If you want to deploy it and track changes, make a fork

```
$ cd <folder_name>
$ git fork
```

##### Step 2. Install on your local machine

To install use
```
$~/path_to_git_clone_folder/ python setup.py install
```

To develop use
```
$~/path_to_git_clone_folder/ python setup.py develop
```

## Quick start

Remove files using "smart_rm" command. Get help example

```
smart_rm -h
usage: smart_rm [-h] [-d] [-r] [-i] [-f] [--regex REGEX]
                [--config CONFIG_FILE_PATH] [--log LOG_FILE_PATH]
                [--log_level] [-s] [--dry_run] [-v]
                path [path ...]

positional arguments:
  path                  Files to be deleted

optional arguments:
  -h, --help            show this help message and exit
  -d, --dir             Remove empty directories
  -r, -R, --recursive   Remove directories and their contents recursively
  -i, --interactive     Prompt before every removal
  -f, --force           Never prompt
  --regex REGEX         Let remove by regular expression
  --config CONFIG_FILE_PATH
                        Path to configuration file for this launch
  --log LOG_FILE_PATH   Path to log file for this launch
  --log_level           Path to log file for this launch
  -s, --silent          Launch in silent mode
  --dry_run             Launch in dry-run mode
  -v, --verbose         Give full description
```

Work with trash using "trash" command. Get help example
```
trash -h
usage: trash [-h] [--clear] [--content]
             [--restore RESTORE_FROM_TRASH [RESTORE_FROM_TRASH ...]]
             [--check_hash] [--config CONFIG_FILE_PATH] [--log LOG_FILE_PATH]
             [--log_level] [-s] [--dry_run] [-v]

optional arguments:
  -h, --help            show this help message and exit
  --clear               Clear trash
  --content             View trash content
  --restore RESTORE_FROM_TRASH [RESTORE_FROM_TRASH ...]
                        Restore files from trash
  --check_hash          Check hash when restore from trash
  --config CONFIG_FILE_PATH
                        Path to configuration file for this launch
  --log LOG_FILE_PATH   Path to log file for this launch
  --log_level           Path to log file for this launch
  -s, --silent          Launch in silent mode
  --dry_run             Launch in dry-run mode
  -v, --verbose         Give full description
```

## Authors

* **Katya Shilovskaya** - *Initial work* - [Kat6123](https://bitbucket.org/kat6123/)
