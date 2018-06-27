# github-label-maker.py - sane labels for GitHub made easy
#
# Written by Mateusz Loskot <mateusz at loskot dot net>
#
# This is free and unencumbered software released into the public domain.
#
import argparse
import logging
import os
import sys
import glm

log = logging.getLogger('glm')

if __name__ == "__main__":
    p = argparse.ArgumentParser(description='Make GitHub labels from definitions in labels/*.json or restore GitHub defaults from labels/default.json')
    p.add_argument('-l', '--make-labels-from', help='Directory of JSON files or single file with definitions of labels')
    p.add_argument('-a', '--make-append', help='Make without clearing existing labels', action='store_true')
    p.add_argument('-d', '--dump-labels-to', help='Dump existing labels to given JSON file')
    p.add_argument('-o', '--owner', help='GitHub repository owner', required=True)
    p.add_argument('-r', '--repository', help='GitHub repository', required=True)
    p.add_argument('-t', '--token', help='GitHub personal access token, if not set in GITHUB_ACCESS_TOKEN environment variable')
    p.add_argument('-v', '--verbose', help='Turn off verbose logging', action='store_true')
    args = p.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    if not args.token and 'GITHUB_ACCESS_TOKEN' in os.environ:
        log.info('reading GITHUB_ACCESS_TOKEN environment variable')
        args.token = os.environ['GITHUB_ACCESS_TOKEN']

    assert args.token, "GitHub token is required for successfull authentication"
    assert args.dump_labels_to or args.make_labels_from

    if args.dump_labels_to:
        dump_file = args.dump_labels_to
        assert dump_file.endswith('json')
        glm.dump(args.token, args.owner, args.repository, dump_file)
    else:
        if os.path.isdir(args.make_labels_from):
            labels_dir = args.make_labels_from
            labels_files = {
                os.path.splitext(f)[0]:
                os.path.join(labels_dir, f)
                    for f in os.listdir(labels_dir) if f.endswith('.json')
            }
        else:
            assert os.path.isfile(args.make_labels_from)
            f = os.path.basename(args.make_labels_from)
            labels_files = {
                os.path.splitext(f)[0]: args.make_labels_from
            }
        glm.make(args.token, args.owner, args.repository, labels_files, args.make_append)
