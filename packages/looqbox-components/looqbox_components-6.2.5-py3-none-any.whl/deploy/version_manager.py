import logging
import re

logger = logging.getLogger("version_manager")


class VersionManager:
    def __init__(self, s3_client, bucket, prefix):
        self.client = s3_client
        self.bucket = bucket
        self.prefix = prefix

    def list_versions(self):
        versions = set()
        version_pattern = re.compile(rf'{self.prefix}(\d+\.\d+\.\d+)/')
        paginator = self.client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=self.bucket, Prefix=self.prefix):
            for obj in page.get('Contents', []):
                match = version_pattern.search(obj['Key'])
                if match:
                    versions.add(match.group(1))
        return versions

    @staticmethod
    def get_latest_version(versions, branch):
        pattern = re.compile(r'v(\d+)\.x')
        if match := pattern.search(branch):
            major_version = match.group(1)
            filtered_versions = [v for v in versions if v.startswith(f"{major_version}.")]
        else:
            logger.warning("Branch name does not match pattern. Using latest version.")
            filtered_versions = versions
        sorted_versions = sorted(filtered_versions, key=lambda x: list(map(int, x.split('.'))))
        return sorted_versions[-1] if filtered_versions else None

    @staticmethod
    def increment_version(version, increment_type, custom_version=None):
        if custom_version:
            return custom_version

        major, minor, patch = map(int, version.split('.'))

        increment_actions = {
            'major': lambda: (major + 1, 0, 0),
            'minor': lambda: (major, minor + 1, 0),
            'patch': lambda: (major, minor, patch + 1),
            'replace': lambda: (major, minor, patch)
        }

        if increment_type in increment_actions:
            major, minor, patch = increment_actions[increment_type]()
        else:
            logger.warning("Invalid increment type. Returning received version.")
            return version

        return f"{major}.{minor}.{patch}"
