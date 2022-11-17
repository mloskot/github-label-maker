# standard lib
import os
import unittest
import warnings

# this package
from gh_label_maker import glm


def ignore_requests_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            test_func(self, *args, **kwargs)
    return do_test

class GithubLaberMakerTest(unittest.TestCase):
    def setUp(self):
        super().setUp()
        script_dir = os.path.dirname(os.path.realpath(__file__))
        token_file = os.path.join(script_dir, '.token')
        if os.path.isfile(token_file):
            with open(token_file) as f:
                self.github_token = f.readline()
            token_file = None
        else:
            self.github_token = os.environ['GITHUB_ACCESS_TOKEN']
        self.assertIsNotNone(self.github_token)
        self.glm = glm.GithubLabelMaker(self.github_token, 'mloskot', 'github-label-maker')

    @ignore_requests_warnings
    def test_A_clear(self):
        self.glm.clear()

    @ignore_requests_warnings
    def test_B_add_label(self):
        label = {"name": "bug", "color": "#fc2929"}
        self.glm.add_label(label)

    @ignore_requests_warnings
    def test_C_edit_label(self):
        label = {"name": "bug", "color": "#ff0000"}
        self.glm.edit_label(label)
        self.assertDictEqual(self.glm.get_label(label['name']), {"name": "bug", "color": "#ff0000", 'description': None})
        label = {"current_name": "bug", "name": "annoyance", "color": "#ff00ff"}
        self.glm.edit_label(label)
        self.assertDictEqual(self.glm.get_label(label['name']), {"name": "annoyance", "color": "#ff00ff", 'description': None})
        label = {"old_name": "annoyance", "name": "bug", "color": "#fc2929"}
        self.glm.edit_label(label)
        self.assertDictEqual(self.glm.get_label(label['name']), {"name": "bug", "color": "#fc2929", 'description': None})

    @ignore_requests_warnings
    def test_D_get_labels(self):
        labels = self.glm.get_labels()
        self.assertEqual(len(labels), 1)
        label = labels[0]
        self.assertDictEqual(label, {'name': 'bug', 'color': '#fc2929', 'description': None})

    @ignore_requests_warnings
    def test_E_add_labels(self):
        # try also colors without hash are fine
        labels = [
            {"name": "feature", "color": "00ff00"},
            {"name": "question", "color": "cc317c"}
        ]
        self.glm.add_labels(labels)

    @ignore_requests_warnings
    def test_F_get_labels(self):
        labels = self.glm.get_labels()
        self.assertEqual(len(labels), 3)
        self.assertEqual(labels, [
            {"name": "bug", "color": "#fc2929", 'description': None},
            {"name": "feature", "color": "#00ff00", 'description': None},
            {"name": "question", "color": "#cc317c", 'description': None}
        ])

    @ignore_requests_warnings
    def test_G_delete_labels(self):
        self.glm.delete_labels(['bug', 'question'])

    @ignore_requests_warnings
    def test_H_get_labels(self):
        labels = self.glm.get_labels()
        self.assertEqual(len(labels), 1)
        self.assertEqual(labels, [
            {"name": "feature", "color": "#00ff00", 'description': None}
        ])

    @ignore_requests_warnings
    def test_I_update_labels(self):
        # try also colors without hash are fine
        labels = [
            {"name": "bug", "color": "#ff0000"},
            {"old_name": "feature", "name": "support", "color": "#000000"},
            {"name": "question", "color": "#0000ff"}
        ]
        self.glm.update_labels(labels)

    @ignore_requests_warnings
    def test_J_get_labels(self):
        labels = self.glm.get_labels()
        self.assertEqual(len(labels), 3)
        self.assertEqual(labels, [
            {"name": "bug", "color": "#ff0000", 'description': None},
            {"name": "question", "color": "#0000ff", 'description': None},
            {"name": "support", "color": "#000000", 'description': None}
        ])
