import os
import unittest
import glm

class GithubLaberMakerTest(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.github_token = os.environ['GITHUB_ACCESS_TOKEN']
        self.assertIsNotNone(self.github_token)
        self.github_owner = 'mloskot'
        self.github_repo  = 'github-label-maker'

    def test_1_clear(self):
        glm.clear(self.github_token, self.github_owner, self.github_repo)

    def test_2_make(self):
        labels = [
            { "name": "bug", "color": "#fc2929" },
            { "name": "question", "color": "#cc317c" }
        ]
        glm.make(self.github_token, self.github_owner, self.github_repo, labels_from = labels)

    def test_3_dump(self):
        pass

    def test_4_edit(self):
        pass
