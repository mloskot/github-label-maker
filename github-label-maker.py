# github-label-maker.py - sane labels for GitHub made easy
#
# Written by Mateusz Loskot <mateusz at loskot dot net>
#
# This is free and unencumbered software released into the public domain.
#
from binascii import crc32
import argparse
import json
import logging
import os
import sys
import github

log = logging.getLogger('glm')

class GitHub:
    def __init__(self, github_token, github_owner_name, github_repo_name):
        assert isinstance(github_owner_name, str)
        assert isinstance(github_repo_name, str)

        g = github.Github(github_token)
        assert g.get_user().login

        log.info("authorized to github as user '%s'", g.get_user().login)
        rate_limit = g.get_rate_limit()
        log.info('rate limit=%d, remaining=%d', rate_limit.rate.limit, rate_limit.rate.remaining)

        # Repository either owned by user or one of user's organization
        orgs = [org.login for org in g.get_user().get_orgs()]
        if github_owner_name in orgs:
            owner = g.get_organization(github_owner_name)
        else:
            owner = g.get_user()
        self.repo = owner.get_repo(github_repo_name)
        log.info("connected to repository '%s/%s'", owner.login, self.repo.name)

    def add_label(self, name, color, description=None):
        if color.startswith('#'):
            color = color[1:]
        if not description:
            description = github.GithubObject.NotSet
        log.info("creating label '%s'", name)
        return self.repo.create_label(name, color, description)

    def add_labels(self, labels):
        for label in labels:
            assert 'name' in label
            assert 'color' in label
            description = None
            if 'description' in label:
                description = label['description']
            self.add_label(label['name'], label['color'], description)

    def delete_labels(self):
        for label in self.repo.get_labels():
            log.info('deleting label %s', label.name)
            label.delete()

    def dump_labels(self):
        labels = []
        repo_labels = self.repo.get_labels()
        for label in repo_labels:
            entry = { "name" : label.name, "color": "#{0}".format(label.color) }
            if label.description is not github.GithubObject.NotSet:
                entry['description'] = label.description
            labels.append(entry)
        return labels

def make(github_token, github_owner, github_repo, labels_from, append_mode=False):
    hub = GitHub(github_token, github_owner, github_repo)
    if not append_mode:
        hub.delete_labels()
    for _, labels_file in labels_from.items():
        log.info("creating labels from '%s'", labels_file)
        with open(labels_file, 'r') as f:
            labels_def = json.load(f)
            hub.add_labels(labels_def)

def dump(github_token, github_owner, github_repo, labels_to):
    hub = GitHub(github_token, github_owner, github_repo)
    labels_def = hub.dump_labels()
    log.info("dumping labels to '%s'", labels_to)
    with open(labels_to, 'w') as f:
        labels_def = json.dumps(labels_def, indent=2)
        f.write(labels_def)

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
        dump(args.token, args.owner, args.repository, dump_file)
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
        make(args.token, args.owner, args.repository, labels_files, args.make_append)
