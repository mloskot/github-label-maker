# github-label-maker

Python script to manage GitHub labels the saner way.

Makes it easy to:

* generate [sane labels](https://medium.com/@dave_lunny/sane-github-labels-c5d2e6004b63) using labels definitions read from JSON files
* dump your existing precious labels into JSON file

## Usage

Output of `python github-label-maker.py -h` should be self-explanatory.

If it is not, there are two modes of operation:

* dump using `--dump-labels-to=/my/labels.json`
* make
  * from single file `--make-labels-from=/my/scheme/default.json`
  * from multiple files `--make-labels-from=/my/scheme`
  * both accept `--make-append` flag to add labels, without prior clearing.
