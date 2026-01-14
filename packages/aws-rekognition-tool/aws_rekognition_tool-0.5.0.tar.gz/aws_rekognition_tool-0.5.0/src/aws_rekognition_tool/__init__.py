"""
AWS Rekognition Tool - Super Simple API!

Simple Usage (No credentials needed):
    from aws_rekognition_tool import detect_labels
    
    result = detect_labels("/path/to/image.jpg")
    result.print_labels()
"""

from .rekognition import (
    AWSRekognition,
    DetectionResult,
    Label,
    # Simple functions - no credentials needed!
    detect_labels,
    detect_faces,
    detect_text,
    analyze_image
)
from .s3_handler import S3Handler
from .config import AWSConfig, RekognitionSettings
from .exceptions import (
    RekognitionToolError,
    AWSCredentialsError,
    ImageNotFoundError,
    S3UploadError,
    S3DeleteError,
    RekognitionError,
    InvalidImageError,
    ImageTooLargeError
)

__version__ = "0.5.0"  # Version update!
__author__ = "Balamurugan"
__email__ = "devteam477@gmail.com"

__all__ = [
    # Simple functions - USERS ITHU USE PANNUVANGA!
    "detect_labels",
    "detect_faces", 
    "detect_text",
    "analyze_image",
    
    # Classes
    "AWSRekognition",
    "DetectionResult",
    "Label",
    "S3Handler",
    "AWSConfig",
    "RekognitionSettings",
    
    # Exceptions
    "RekognitionToolError",
    "AWSCredentialsError",
    "ImageNotFoundError",
    "S3UploadError",
    "S3DeleteError",
    "RekognitionError",
    "InvalidImageError",
    "ImageTooLargeError",
]