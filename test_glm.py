import os
import unittest
import glm

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
        self.github_owner = 'mloskot'
        self.github_repo  = 'github-label-maker'

    def test_1_clear(self):
        glm.clear(self.github_token, self.github_owner, self.github_repo)

    def test_2_make_one(self):
        label_def = { "name": "bug", "color": "#fc2929" }
        glm.make(self.github_token, self.github_owner, self.github_repo, label_def, append_mode=False)

    def test_3_dump(self):
        labels = glm.dump(self.github_token, self.github_owner, self.github_repo)
        self.assertEqual(len(labels), 1)
        label = labels[0]
        self.assertDictEqual(label, {'name': 'bug', 'color': '#fc2929', 'description': None})

    def test_4_make_multiple(self):
        # try colors without hash
        labels_def = [
            {"name": "feature", "color": "00ff00"},
            {"name": "question", "color": "cc317c"}
        ]
        glm.make(self.github_token, self.github_owner,
                 self.github_repo, labels_def, append_mode=False)

    def test_5_dump(self):
        labels = glm.dump(self.github_token,
                          self.github_owner, self.github_repo)
        self.assertEqual(len(labels), 2)
        self.assertEqual(labels, [
            {"name": "feature", "color": "#00ff00", 'description': None},
            {"name": "question", "color": "#cc317c", 'description': None}
        ])

    def test_6_append_one(self):
        label_def = { "name": "bug", "color": "#fc2929" }
        glm.make(self.github_token, self.github_owner, self.github_repo, label_def, append_mode=True)

    def test_7_dump(self):
        labels = glm.dump(self.github_token,
                          self.github_owner, self.github_repo)
        self.assertEqual(len(labels), 3)
        self.assertEqual(labels, [
            {"name": "bug", "color": "#fc2929", 'description': None},
            {"name": "feature", "color": "#00ff00", 'description': None},
            {"name": "question", "color": "#cc317c", 'description': None}
        ])

    def test_8_edit(self):
        pass
