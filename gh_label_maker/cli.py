# github-label-maker.py - sane labels for GitHub made easy
#
# Written by Mateusz Loskot <mateusz at loskot dot net>
#
# This is free and unencumbered software released into the public domain.

# std lib
import argparse
import json
import logging
import os

# this package
from gh_label_maker import glm

def run():
    p = argparse.ArgumentParser(description='Make GitHub labels from definitions in labels/*.json or restore GitHub defaults from labels/default.json')
    p.add_argument('-v', '--verbose', help='Turn off verbose logging', action='store_true')
    p.add_argument('-o', '--owner', help='GitHub repository owner', required=True)
    p.add_argument('-r', '--repository', help='GitHub repository', required=True)
    p.add_argument('-t', '--token', help='GitHub personal access token, if not set in GITHUB_ACCESS_TOKEN environment variable')
    p.add_argument('-c', '--clear-labels', help='Clear all labels', action='store_true')
    p.add_argument('-m', '--make-labels-from', help='Create labels from definitions in specified JSON file or directory of files')
    p.add_argument('-d', '--dump-labels-to', help='Dump existing labels to given JSON file')
    args = p.parse_args()

    if args.verbose:
        glm.set_verbose_logging()

    if not args.token:
        if 'GITHUB_ACCESS_TOKEN' in os.environ:
            logging.info('reading GITHUB_ACCESS_TOKEN environment variable')
            args.token = os.environ['GITHUB_ACCESS_TOKEN']
        else:
            script_dir = os.path.dirname(os.path.realpath(__file__))
            token_file = os.path.join(script_dir, '.token')
            if os.path.isfile(token_file):
                with open(token_file) as f:
                    args.token = f.readline()
    assert args.token, "GitHub token is required for successfull authentication"
    assert args.clear_labels or args.dump_labels_to or args.make_labels_from

    hub = glm.GithubLabelMaker(args.token, args.owner, args.repository, verbose=args.verbose)

    if args.clear_labels:
        logging.info("deleting all labels")
        hub.clear()
    elif args.dump_labels_to:
        assert args.dump_labels_to.endswith('json')
        labels_def = hub.get_labels()
        if labels_def:
            logging.info("dumping labels to '{0}'".format(args.dump_labels_to))
            with open(args.dump_labels_to, 'w') as f:
                labels_def = json.dumps(labels_def, indent=2)
                f.write(labels_def)
        else:
            logging.info("no labels found")
    else:
        if os.path.isdir(args.make_labels_from):
            labels_dir = args.make_labels_from
            labels_def_files = [
                os.path.join(labels_dir, f)
                    for f in os.listdir(labels_dir) if f.endswith('.json')
            ]
        else:
            assert os.path.isfile(args.make_labels_from)
            labels_def_files = [ args.make_labels_from ]

        for labels_file in labels_def_files:
            logging.info("creating labels from '%s'", labels_file)
            with open(labels_file, 'r') as f:
                labels_def = json.load(f)
                hub.update_labels(labels_def)


if __name__ == "__main__":
    run()