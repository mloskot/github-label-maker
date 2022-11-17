# glm.py - GitHub Labels Maker module for easy labels management
#
# Written by Mateusz Loskot <mateusz at loskot dot net>
#
# This is free and unencumbered software released into the public domain.
#
import logging
import github

def set_verbose_logging():
    logging.basicConfig(level=logging.INFO)

class GithubLabelMaker:
    def __init__(self, github_token, github_owner_name, github_repo_name, verbose=False):
        assert isinstance(github_owner_name, str)
        assert isinstance(github_repo_name, str)

        if verbose:
            set_verbose_logging()

        g = github.Github(github_token)
        assert g.get_user().login

        logging.info("authorized to github as user '{0}'".format(g.get_user().login))
        rate_limit = g.get_rate_limit()
        logging.info('rate limit={0}, remaining={1}'.format(rate_limit.core.limit, rate_limit.core.remaining))

        # Repository either owned by user or one of user's organization
        orgs = [org.login for org in g.get_user().get_orgs()]
        if github_owner_name in orgs:
            owner = g.get_organization(github_owner_name)
        else:
            owner = g.get_user()
        self._repo = owner.get_repo(github_repo_name)
        logging.info("connected to repository '{0}/{1}'".format(owner.login, self._repo.name))

    def _find_label(self, name):
        try:
            if name is None:
                name = ''
            return self._repo.get_label(name)
        except github.UnknownObjectException as e:
            logging.info(e)
            logging.info("label '{0}' not found".format(name))
            return None

    def _get_labels_def(self, labels_from):
        assert labels_from
        if isinstance(labels_from, dict):
            labels_def = [labels_from]
        else:
            labels_def = labels_from
        assert isinstance(labels_from, list)
        assert isinstance(labels_from[0], dict)
        return labels_def

    def _get_label_properties(self, label_def):
        assert isinstance(label_def, dict)
        assert 'name' in label_def
        assert 'color' in label_def
        name = label_def['name']
        color = label_def['color']
        if color.startswith('#'):
            color = color[1:]
        description = github.GithubObject.NotSet
        if 'description' in label_def:
            description = label_def['description']
        old_name = name
        if 'old_name' in label_def:
            old_name = label_def['old_name']
        elif 'current_name' in label_def:
            old_name = label_def['current_name']
        return name, color, description, old_name

    def add_label(self, label_def):
        name, color, description, *_ = self._get_label_properties(label_def)
        logging.info("adding label '{0}'".format(name))
        self._repo.create_label(name, color, description)

    def add_labels(self, labels_def):
        labels_def = self._get_labels_def(labels_def)
        for label_def in labels_def:
            self.add_label(label_def)

    def clear(self):
        for label in self._repo.get_labels():
            logging.info("deleting label '{0}'".format(label.name))
            label.delete()

    def delete_label(self, label_def_or_name):
        if isinstance(label_def_or_name, str):
            name = label_def_or_name
        else:
            name, *_ = self._get_label_properties(label_def_or_name)
        label = self._find_label(name)
        if label:
            logging.info("deleting label '{0}'".format(name))
            label.delete()
            return True
        else:
            return False

    def delete_labels(self, labels_def_or_names):
        for def_or_name in labels_def_or_names:
            self.delete_label(def_or_name)

    def edit_label(self, label_def):
        name, color, description, old_name = self._get_label_properties(label_def)
        label = self._find_label(old_name)
        if label:
            logging.info("editing label '{0}' as '{1}'".format(old_name, name))
        else:
            label = self._find_label(name)
            if label:
                logging.info("editing label '{0}'".format(name))

        if label:
            label.edit(name, color, description)
            return True
        else:
            logging.info("label '{0}' not found to edit as '{1}'".format(old_name, name))
            return False

    def edit_labels(self, labels_def):
        labels_def = self._get_labels_def(labels_def)
        for label_def in labels_def:
            self.edit_label(label_def)

    def get_label(self, name):
        label = self._find_label(name)
        if not label:
            logging.info("label '{0}' not found".format(name))
        label_def = { "name" : label.name, "color": "#{0}".format(label.color) }
        if label.description is not github.GithubObject.NotSet:
            label_def['description'] = label.description
        return label_def

    def get_labels(self):
        labels_def = []
        repo_labels = self._repo.get_labels()
        for label in repo_labels:
            label_def = { "name" : label.name, "color": "#{0}".format(label.color) }
            if label.description is not github.GithubObject.NotSet:
                label_def['description'] = label.description
            labels_def.append(label_def)
        return labels_def

    def update_label(self, label_def):
        if not self.edit_label(label_def):
            self.add_label(label_def)

    def update_labels(self, labels_def):
        for label_def in labels_def:
            self.update_label(label_def)
