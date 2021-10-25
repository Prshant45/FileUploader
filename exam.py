import pathlib
import os
import json 
from abc import ABC, abstractmethod

import boto3
from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials

class CustomException(Exception):
    """Custom Exception for raise the exception"""
    pass

class FileUploader(ABC):
    """Basic representation of file uploader."""
    
    @abstractmethod
    def set_credentials(self, credentials_file: pathlib.Path = None):
        """set credentials for specific bucket."""
    
    @abstractmethod
    def connect(self):
        """connect to specific bucket."""

    @abstractmethod
    def upload(self, file_name: pathlib.Path):
        """upload the file to specific bucket."""
        

class S3Bucket(FileUploader):
    """Basic representation of S3 bucket file uploader."""


    def set_credentials(self, credentials_file: pathlib.Path = None):
        """set credentials for specific bucket."""
        if credentials_file:
            with open(credentials_file, 'r') as fp:
                self.credentials = json.loads(fp.read())
        else:
            self.credentials = os.environ["S3_CREDENTIALS"]


    def connect(self):
        """connect to s3 bucket."""
        try:
            self.client = boto3.resource(
                    service_name='s3',
                    #region_name=self.credentials['region_name'],
                    aws_access_key_id=self.credentials['aws_access_key_id'],
                    aws_secret_access_key=self.credentials['aws_secret_access_key']
                )
        except Exception as e:
            print(e)

    def upload(self, file_name: pathlib.Path):
        """upload the file to s3 bucket."""
        try:
            self.client.Bucket(self.credentials['bucket_name']).upload_file(Filename=file_name, Key=os.path.basename(file_name))
        except Exception as e:
            print(e)
            
        

class GoogleStorage(FileUploader):
    """Basic representation of Google storage file uploader."""

    def set_credentials(self, credentials_file: pathlib.Path = None):
        """set credentials for specific bucket.
        credentials_dict = {
            'type': 'service_account',
            'client_id': 'client_id',
            'client_email': 'client_email',
            'private_key_id': 'private_key_id',
            'private_key': 'private_key',
            }
        """
        if credentials_file:
            with open(credentials_file, 'r') as fp:
                self.credentials = json.loads(fp.read())
        else:
            self.credentials = os.environ["GOOGLE_STORAGE_CREDENTIALS"]

    def connect(self):
        """connect to google storage."""
        try:
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(self.credentials['json_auth'])
            self.client = storage.Client(credentials=credentials, project=self.credentials['project_name'])
            self.bucket = client.get_bucket(self.credentials['bucket_name'])
        except Exception as e:
            print(e)

    def upload(self, file_name: pathlib.Path):
        """upload the file to google storage."""
        try:
            blob = self.bucket.blob(os.path.basename(file_name))
            blob.upload_from_filename(file_name)
        except Exception as e:
            print(e)
        

class UploaderCreator(ABC):
    """Object Creator of various uploader"""
    
    @abstractmethod
    def get_object(self) -> FileUploader:
        """Returns a new file uploader."""
        
    @abstractmethod
    def get_file_config(self) -> list:
        """Returns a new file configuration."""

class S3UploaderCreator(UploaderCreator):
    """used to create the S3 object"""
    
    def get_object(self) -> FileUploader:
        """Returns a new file uploader."""
        path = input("Enter the credentials file path of s3 bucket or press enter to skip if credentials are in OS env: ")
        s3_bucket = S3Bucket()
        if path:
            s3_bucket.set_credentials(path)
        else:
            s3_bucket.set_credentials()
        s3_bucket.connect()
        return s3_bucket

    def get_file_config(self) -> list:
        """Returns a new file configuration."""
        path = input("Enter the configuration file path for s3 bucket or press enter to skip if want to use default: ")
        s3_list_extension = []
        if not path:
            path = 's3_file.txt'
        with open(path) as fp:
            s3_list_extension = [n.strip() for n in fp.readlines()]
        return s3_list_extension

class GStorageUploaderCreator(UploaderCreator):
    """used to create the S3 object"""
    
    def get_object(self) -> FileUploader:
        """Returns a new file uploader."""  
        path = input("Enter the credentials file path for google storage or press enter to skip if credentials are in OS env: ")
        g_storage = GoogleStorage()
        if path:
            g_storage.set_credentials(path)
        else:
            g_storage.set_credentials()
        g_storage.connect()
        return g_storage
    
    def get_file_config(self) -> list:
        """Returns a new file configuration."""
        path = input("Enter the configuration file path for Google storage or press enter to skip if want to use default: ")
        s3_list_extension = []
        if not path:
            path = 'g_file.txt'
        with open(path) as fp:
            s3_list_extension = [n.strip() for n in fp.readlines()]
            
        return s3_list_extension

def get_storage_config() -> dict:
    """get storage configuration."""
    s3 = S3UploaderCreator()
    gstorage = GStorageUploaderCreator()
    storages = {'s3': [s3.get_file_config(), s3.get_object()],
                'g_storage': [gstorage.get_file_config(), gstorage.get_object()]
                }
    return storages

def upload_files(path: pathlib.Path,storages: dict) -> bool:
    """upload the files in respective storage."""
    for abs_path, current_dir, curr_dir_files in os.walk(path):
        for current_file in curr_dir_files:
            extension = os.path.splitext(current_file)[1]
            if extension in storages['s3'][0]:
                
                storages['s3'][1].upload(os.path.join(abs_path, current_file))
            elif extension in storages['g_storage'][0]:
                storages['g_storage'][1].upload(os.path.join(current_dir, current_file))
    return True


def main():
    path = input("Please enter the path of files that need to be uploaded: ")
    storages = get_storage_config()
    if upload_files(path, storages):
        print("uploaded successfully")
    else:
        print("something went wrong")
    
if __name__ == "__main__":

    # perform the uploading job
    main()