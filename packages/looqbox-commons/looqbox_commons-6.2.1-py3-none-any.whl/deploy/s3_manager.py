import logging
import os

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger("s3_manager")


class S3Manager:
    def __init__(self, bucket_name):
        self.client = boto3.client(
            's3',
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
        )
        self.bucket_name = bucket_name

    @staticmethod
    def is_test_file(file_name):
        return "test.py" in file_name or "teste.py" in file_name

    @staticmethod
    def remove_pycache(directories):
        try:
            directories.remove("__pycache__")
        except ValueError:
            pass

    def upload_file(self, file_name, object_name=None):
        if object_name is None:
            object_name = os.path.basename(file_name)

        if self.is_test_file(file_name):
            return True

        try:
            self.client.upload_file(file_name, self.bucket_name, object_name)
        except ClientError as e:
            logger.error(e)
            return False

        return True

    def upload_dir(self, dir_name, s3_dir_name=None, absolute_path=None):
        if absolute_path is None:
            absolute_path = dir_name

        _, directories, files = next(os.walk(dir_name))

        s3_dir_name = s3_dir_name or os.path.basename(os.path.normpath(dir_name))

        self.remove_pycache(directories)
        for directory in directories:
            children_dir = os.path.join(dir_name, directory)
            children_s3_path = os.path.join(s3_dir_name, directory)
            self.upload_dir(children_dir, children_s3_path, absolute_path)

        for file in files:
            file_s3_path = os.path.join(s3_dir_name, file)
            file_path = os.path.join(absolute_path, dir_name, file)
            if not self.upload_file(file_path, file_s3_path):
                return False

        return True


def define_s3_bucket(argv):
    if "prod" in argv or "production" in argv:
        return "looqbox-dynamic-packages"
    elif "dev" in argv or "development" in argv:
        return "looqbox-dynamic-packages-development"
    else:
        raise ValueError("Please choose production or development context")
