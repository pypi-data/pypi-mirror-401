"""
S3 Handler - S3 operations ellam inga handle panrom
"""

import os
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from typing import Optional

from .exceptions import (
    S3UploadError,
    S3DeleteError,
    ImageNotFoundError,
    AWSCredentialsError
)
from .config import AWSConfig


class S3Handler:
    """
    S3 operations ku oru separate class
    
    Usage:
        handler = S3Handler(config)
        s3_key = handler.upload_image("/path/to/image.jpg")
        handler.delete_image(s3_key)
    """
    
    def __init__(self, config: AWSConfig):
        """
        S3Handler initialize pannum
        
        Args:
            config: AWSConfig object with credentials
        """
        self.config = config
        self._client = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """S3 client create pannum"""
        try:
            self._client = boto3.client(
                's3',
                region_name=self.config.region_name,
                aws_access_key_id=self.config.aws_access_key_id,
                aws_secret_access_key=self.config.aws_secret_access_key
            )
        except NoCredentialsError:
            raise AWSCredentialsError("AWS credentials illa! Check pannunga.")
        except Exception as e:
            raise AWSCredentialsError(f"AWS client create aagala: {e}")
    
    @property
    def client(self):
        """S3 client return pannum"""
        return self._client
    
    def upload_image(self, local_path: str, custom_key: Optional[str] = None) -> str:
        """
        Local image ah S3 ku upload pannum
        
        Args:
            local_path: Local file path
            custom_key: Custom S3 key (optional)
        
        Returns:
            S3 object key
        
        Raises:
            ImageNotFoundError: File illa na
            S3UploadError: Upload fail aana
        """
        # File exists ah check pannunga
        if not os.path.exists(local_path):
            raise ImageNotFoundError(f"Image file illa: {local_path}")
        
        # S3 key generate pannunga
        if custom_key:
            s3_key = custom_key
        else:
            filename = os.path.basename(local_path)
            s3_key = f"{self.config.s3_folder}{filename}"
        
        try:
            self._client.upload_file(
                local_path,
                self.config.bucket_name,
                s3_key
            )
            return s3_key
            
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            raise S3UploadError(f"S3 upload fail [{error_code}]: {e}")
        except Exception as e:
            raise S3UploadError(f"Upload error: {e}")
    
    def delete_image(self, s3_key: str) -> bool:
        """
        S3 la irundhu image delete pannum
        
        Args:
            s3_key: S3 object key
        
        Returns:
            True if successful
        
        Raises:
            S3DeleteError: Delete fail aana
        """
        try:
            self._client.delete_object(
                Bucket=self.config.bucket_name,
                Key=s3_key
            )
            return True
            
        except ClientError as e:
            raise S3DeleteError(f"S3 delete fail: {e}")
        except Exception as e:
            raise S3DeleteError(f"Delete error: {e}")
    
    def check_bucket_exists(self) -> bool:
        """Bucket exists ah check pannum"""
        try:
            self._client.head_bucket(Bucket=self.config.bucket_name)
            return True
        except ClientError:
            return False
    
    def list_images(self, prefix: str = "") -> list:
        """S3 bucket la images list pannum"""
        try:
            response = self._client.list_objects_v2(
                Bucket=self.config.bucket_name,
                Prefix=prefix or self.config.s3_folder
            )
            
            if 'Contents' not in response:
                return []
            
            return [obj['Key'] for obj in response['Contents']]
            
        except ClientError as e:
            raise S3UploadError(f"List objects fail: {e}")