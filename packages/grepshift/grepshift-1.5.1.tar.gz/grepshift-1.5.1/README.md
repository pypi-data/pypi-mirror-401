# grepshift

grepshift finds and replaces all instances of a string with a new string in a directory and all its sub-directories. The followinmg directories
are excluded: .git, .hg, .svn, .vscode, .idea, .metadata, node_modules, .gradle, .m2, .venv, venv, \_\_pycache\_\_.


```
Usage:
    grepshift [options] <pattern> [<replacement>]

Options:
    -d, --directory=<directory>   Starting directory [default: .]
    -e, --extension=<extension>   Only process file with this extension
    -h, --help                    Show this help screen
    -l, --list                    Just list the files to be changed, no actual changes
    -r, --remove                  Removes the line, that matches pattern, from all files
    -v, --verbose                 Verbose Mode
    --version                     Prints the version
```

## Installation

```bash
pip install grepshift
```

## License

grepshift is freeware released under the [MIT License](https://github.com/scholnicks/grepshift/blob/main/LICENSE).
