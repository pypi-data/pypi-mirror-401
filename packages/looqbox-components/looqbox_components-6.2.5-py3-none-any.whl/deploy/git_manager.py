import logging
import os

from git import Repo, GitCommandError



class GitManager:
    def __init__(self):
        # Set up logging
        self.logger = logging.getLogger("git_manager")
        self.current_branch = os.environ['BRANCH']

        # Determine the base directory of the repository
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.repo = Repo(base_dir)
        self.logger.info("Initialized GitManager for repository at: %s", base_dir)

    def __setup_credentials(self):
        try:
            github_token = os.environ['PAT_GIT']
            remote_url = self.repo.remotes.origin.url
            remote_url_with_token = f"https://{github_token}@{remote_url.replace('git@', '').replace(':', '/')}"
            self.repo.remotes.origin.set_url(remote_url_with_token)
            self.logger.info("Remote set to %s", self.repo.remotes.origin.url)
        except Exception as e:
            self.logger.error(str(e))

    def checkout_to_branch(self):
        self.__setup_credentials()
        self.repo.git.checkout(self.current_branch)
        self.logger.info("Checking out to %s", self.current_branch)

    def commit_changes(self, commit_message, file_paths):
        try:
            self.repo.index.add(file_paths)
            self.logger.info("Staged files for commit: %s", file_paths)

            self.repo.index.commit(commit_message)
            self.logger.info("Committed successfully: '%s'", commit_message)
        except GitCommandError as e:
            self.logger.error("Error in git operation: %s", e)

    def push_to_remote(self, remote_name='origin'):
        try:
            origin = self.repo.remote(name=remote_name)
            push_info = origin.push()
            for info in push_info:
                if info.flags & info.ERROR:
                    self.logger.error("Error pushing to remote '%s': %s", remote_name, info.summary)
                else:
                    self.logger.info("Pushed %s to remote '%s': %s", info.local_ref, remote_name, info.summary)
        except GitCommandError as e:
            self.logger.error("Error pushing to remote '%s': %s", remote_name, e)
            return False
        return True
