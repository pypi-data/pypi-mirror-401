import os
import re


class ReadmeUpdater:
    def __init__(self):
        # Determine the base directory of the repository (parent of the 'deploy' directory)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.readme_path = os.path.join(base_dir, 'README.md')

    def update_version(self, new_version):
        # Read the current contents of the README file
        with open(self.readme_path, 'r', encoding='utf-8') as file:
            contents = file.read()

        # Use regular expression to find and replace the version number
        pattern = r'(https://img.shields.io/badge/version-)([\d.]+)(-brightgreen.svg)'
        new_contents = re.sub(pattern, r'\g<1>' + new_version + r'\g<3>', contents)

        # Write the updated contents back to the README file
        with open(self.readme_path, 'w', encoding='utf-8') as file:
            file.write(new_contents)
