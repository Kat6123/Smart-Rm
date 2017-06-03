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

### Utility
#### 1. Use
Remove files using "smart_rm" command.

```
    $ smart_rm file1 file2
    $ smart_rm -d dir1 /home/usr/dir2 --regex 'dir\d+'
```

Work with trash using "trash" command. Without flags it output trash content.
```
    $ trash
```
```
    $ trash --restore file1 file2 dir1
    $ trash --clear
```

For additional information use '-h' option.
```
    $ smart_rm -h
```
```
    $ trash -h
```

#### 2. Make settings
You can find example in 'config/config.cfg'.
To override parametrs for specific utility launch use config flag.

```
    $ smart_rm file1 --config <path_to_config>
```

##### Config sections:
###### [Remove]

Aim indicates smart_rm target object. Can be 'file', 'directory', 'tree'.

``` aim: file```

Mode can be:
'not_write_acces' - confirm deletion if file has no rights to write,
'interactive' - confirm deletion always,
'force' - never confirm.

```mode: not_write_access```

###### [Path to]

```trash: ~/.local/share/trash```

###### [Policies]
Can be 'time' or 'size_time' policy

```clean: size_time```


'size_time' policy clean parametr is maximum size if trash in bytes;
'time' policy clean parametr is maximum time in trash

```clean_parametr: 100```

Define trash behaviour if there are already exists file with same name.
Possible values:
    'ask_new_name', 'give_new_name_depending_on_same_amount',
    'skip', 'replace_without_confirm', 'confirm_and_replace'.

```solve_name_conflict: give_new_name_depending_on_same_amount```

Parametrs for autocleaning.

```max_size: 100```

```max_time_in_trash: 12 months 1 days 2 hours 1 minutes```

### Library
To take advantage of library use 'simple_rm.trash' module.
It provides Trash, TrashInfo classes to work with Trash interface.

    from simple_rm.trash import (
        Trash,
        TrashInfo
    )

Trash class has methods remove, restore, view, clean trash. 
All methods return list of TrashInfo objects.

Trash will use defaults. If not override them it will be created on '~/.local/share/trash' path and remove only list of files.

        my_trash = Trash()
        removed = my_trash.remove([file_path, "not_exist", "hello"])

TrashInfo object is associated with file.
You can use this object to get more information about the file.
If there were errors they append to errors attribute of TrashInfo object.

        for rm_obj in removed:
            if rm_obj.errors:
                for err in rm_obj.errors:
                    print err
            else:
                print rm_obj

Attribute 'errors' can contain instances of classes
from 'simple_rm.error' module.

Further information in Trash and TrashInfo docstrings.

## Authors

* **Katya Shilovskaya** - *Initial work* - [Kat6123](https://bitbucket.org/kat6123/)