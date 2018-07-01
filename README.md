# github-label-maker

Python script to manage GitHub labels the saner way.

Makes it easy to:

* create or edit [sane labels](https://medium.com/@dave_lunny/sane-github-labels-c5d2e6004b63) using labels definitions in JSON files
* dump your existing precious labels into JSON file

## Usage

Output of `python github-label-maker.py -h` should be self-explanatory.

If it is not, there are two modes of operation:

* clear all labels using `--clear`
* add or update labels from files with labels definitions
  * from single file `--make-labels-from=/my/scheme/default.json`
  * from multiple files `--make-labels-from=/my/scheme`
* dump all labels using `--dump-labels-to=/my/labels.json`
