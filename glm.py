# glm.py - GitHub Labels Maker module for easy labels management
#
# Written by Mateusz Loskot <mateusz at loskot dot net>
#
# This is free and unencumbered software released into the public domain.
#
import json
import logging
import github

log = logging.getLogger('glm')

class GithubLabelMaker:
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

    def delete_label(self, name):
        log.info("deleting label '{0}'".format(name))
        label = self.get_label(name)
        if label:
            label.delete()

    def delete_labels(self):
        for label in self.repo.get_labels():
            log.info('deleting label %s', label.name)
            label.delete()

    def get_label(self, name):
        try:
            return self.repo.get_label(name)
        except github.UnknownObjectException as e:
            logging.info(e)
            log.info("label '{0}' not found".format(name))
            return None

    def get_labels(self):
        labels = []
        repo_labels = self.repo.get_labels()
        for label in repo_labels:
            entry = { "name" : label.name, "color": "#{0}".format(label.color) }
            if label.description is not github.GithubObject.NotSet:
                entry['description'] = label.description
            labels.append(entry)
        return labels

    def update_label(self, name, new_name, new_color, new_description=None):
        if new_color.startswith('#'):
            new_color = new_color[1:]
        if not new_description:
            new_description = github.GithubObject.NotSet
        log.info("updating label '{0}' to '{1}'".format(name, new_name))
        label = self.get_label(name)
        if label:
            label.edit(new_name, new_color, new_description)

def clear(github_token, github_owner, github_repo, labels_from=None):
    hub = GithubLabelMaker(github_token, github_owner, github_repo)
    if not labels_from:
        hub.delete_labels()
    else:
        # TODO
        pass

def make(github_token, github_owner, github_repo, labels_from, append_mode=False):
    assert labels_from
    if isinstance(labels_from, dict):
        labels_def = [labels_from]
    else:
        labels_def = labels_from
        assert isinstance(labels_from, list)
        assert isinstance(labels_from[0], dict)
    hub = GithubLabelMaker(github_token, github_owner, github_repo)
    if not append_mode:
        hub.delete_labels()
    hub.add_labels(labels_def)

def make_from_files(github_token, github_owner, github_repo, labels_from, append_mode=False):
    for _, labels_file in labels_from.items():
        log.info("creating labels from '%s'", labels_file)
        with open(labels_file, 'r') as f:
            labels_def = json.load(f)
            make(github_token, github_owner, github_repo, labels_def, append_mode)

def dump(github_token, github_owner, github_repo):
    hub = GithubLabelMaker(github_token, github_owner, github_repo)
    labels_def = hub.get_labels()
    return labels_def

def dump_to_file(github_token, github_owner, github_repo, labels_to):
    labels_def = dump(github_token, github_owner, github_repo)
    if labels_def:
        log.info("dumping labels to '%s'", labels_to)
        with open(labels_to, 'w') as f:
            labels_def = json.dumps(labels_def, indent=2)
            f.write(labels_def)
    else:
        log.info("no labels to dump to '%s'", labels_to)
