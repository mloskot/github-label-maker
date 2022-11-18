# github-label-maker

Python module and script to manage GitHub labels the saner way:

* create or edit [sane labels](https://medium.com/@dave_lunny/sane-github-labels-c5d2e6004b63) using labels definitions in JSON files
* dump your existing precious labels into JSON file

## Requirements

* [PyGithub](https://github.com/PyGithub/PyGithub) 1.56

## Installation

`pip install gh-label-maker`

## Usage

Output of `python github-label-maker.py -h` should be self-explanatory.

If it is not, there are three modes of operation:

* clear all labels using `--clear`
* add or update labels from files with labels definitions
  * from single file `--make-labels-from=/my/scheme/default.json`
  * from multiple files `--make-labels-from=/my/scheme`
* dump all labels using `--dump-labels-to=/my/labels.json`

## Contribute

```bash
# get the source
git clone https://github.com/mloskot/github-label-maker.git

# install source in editable mode 
cd github-label-maker
pip install -e .

# develop and make a pull request!
```

## Credits

- [@GlennWSo](https://github.com/GlennWSo) contributed fixes, release and package for PIP
