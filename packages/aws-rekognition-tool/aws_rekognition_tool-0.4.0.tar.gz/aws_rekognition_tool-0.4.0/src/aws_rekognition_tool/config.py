"""
Configuration - Default credentials embedded
"""
import os
from pathlib import Path
from dataclasses import dataclass

# Load .env file
try:
    from dotenv import load_dotenv
    
    # .env file path find pannunga
    env_path = Path(__file__).parent.parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    else:
        # Current directory la paaru
        load_dotenv()
except ImportError:
    pass  # dotenv illa na skip
from typing import Optional


# ============================================
# 🔐 YOUR CREDENTIALS - EMBED HERE
# ============================================
DEFAULT_AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
DEFAULT_AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "") # Unga Secret Key
DEFAULT_S3_BUCKET_NAME = "aidermatologistsnew"               # Unga Bucket
DEFAULT_REGION = "us-east-1"                                  # Unga Region
DEFAULT_S3_FOLDER = "rekognition_images/"


@dataclass
class AWSConfig:
    """AWS Configuration class"""
    aws_access_key_id: str = DEFAULT_AWS_ACCESS_KEY_ID
    aws_secret_access_key: str = DEFAULT_AWS_SECRET_ACCESS_KEY
    region_name: str = DEFAULT_REGION
    bucket_name: str = DEFAULT_S3_BUCKET_NAME
    s3_folder: str = DEFAULT_S3_FOLDER
    
    def validate(self) -> bool:
        """Credentials check"""
        if not self.aws_access_key_id or not self.aws_secret_access_key:
            return False
        if not self.bucket_name:
            return False
        return True


@dataclass
class RekognitionSettings:
    """Rekognition API settings"""
    max_labels: int = 10
    min_confidence: float = 75.0
    detect_faces: bool = False
    detect_text: bool = False
    detect_moderation: bool = False


SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png']
MAX_IMAGE_SIZE_MB = 15