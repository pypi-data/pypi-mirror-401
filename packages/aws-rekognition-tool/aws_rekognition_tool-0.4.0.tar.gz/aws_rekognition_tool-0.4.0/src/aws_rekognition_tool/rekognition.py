"""
Main Rekognition Module - Simple API with embedded credentials
"""

import os
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from .config import (
    AWSConfig, 
    RekognitionSettings, 
    SUPPORTED_IMAGE_FORMATS,
    DEFAULT_AWS_ACCESS_KEY_ID,
    DEFAULT_AWS_SECRET_ACCESS_KEY,
    DEFAULT_S3_BUCKET_NAME,
    DEFAULT_REGION,
    DEFAULT_S3_FOLDER
)
from .s3_handler import S3Handler
from .exceptions import (
    RekognitionError,
    InvalidImageError,
    ImageTooLargeError,
    AWSCredentialsError,
    ImageNotFoundError
)


@dataclass
class Label:
    """Detected label"""
    name: str
    confidence: float
    parents: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'confidence': self.confidence,
            'parents': self.parents
        }


@dataclass
class DetectionResult:
    """Rekognition result"""
    labels: List[Label] = field(default_factory=list)
    image_path: str = ""
    s3_key: str = ""
    success: bool = False
    error_message: str = ""
    
    def to_dict(self) -> Dict:
        return {
            'success': self.success,
            'image_path': self.image_path,
            's3_key': self.s3_key,
            'labels': [label.to_dict() for label in self.labels],
            'error_message': self.error_message
        }
    
    def print_labels(self) -> None:
        """Print labels nicely"""
        if not self.labels:
            print("No labels detected!")
            return
        
        print(f"\n{'='*50}")
        print(f"Detected Labels for: {self.image_path}")
        print(f"{'='*50}")
        
        for label in self.labels:
            print(f"\n  🏷️  Label: {label.name}")
            print(f"      Confidence: {label.confidence:.2f}%")
            if label.parents:
                print(f"      Parents: {', '.join(label.parents)}")
        
        print(f"\n{'='*50}")
    
    def get_label_names(self) -> List[str]:
        """Just label names return pannum"""
        return [label.name for label in self.labels]


class AWSRekognition:
    """
    AWS Rekognition class - Default credentials embedded
    
    Simple Usage (No credentials needed):
        from aws_rekognition_tool import AWSRekognition
        
        rekognition = AWSRekognition()
        result = rekognition.detect_labels("/path/to/image.jpg")
        result.print_labels()
    """
    
    def __init__(
        self,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        bucket_name: str = None,
        region_name: str = None,
        s3_folder: str = None,
        max_labels: int = 10,
        min_confidence: float = 75.0,
        auto_cleanup: bool = True
    ):
        """
        Initialize - All parameters optional (defaults embedded)
        """
        # Use defaults if not provided
        self.config = AWSConfig(
            aws_access_key_id=aws_access_key_id or DEFAULT_AWS_ACCESS_KEY_ID,
            aws_secret_access_key=aws_secret_access_key or DEFAULT_AWS_SECRET_ACCESS_KEY,
            region_name=region_name or DEFAULT_REGION,
            bucket_name=bucket_name or DEFAULT_S3_BUCKET_NAME,
            s3_folder=s3_folder or DEFAULT_S3_FOLDER
        )
        
        self.settings = RekognitionSettings(
            max_labels=max_labels,
            min_confidence=min_confidence
        )
        
        self.auto_cleanup = auto_cleanup
        
        # Initialize clients
        self._s3_handler = None
        self._rekognition_client = None
        self._initialize_clients()
    
    def _initialize_clients(self) -> None:
        """AWS clients initialize"""
        try:
            self._s3_handler = S3Handler(self.config)
            
            self._rekognition_client = boto3.client(
                'rekognition',
                region_name=self.config.region_name,
                aws_access_key_id=self.config.aws_access_key_id,
                aws_secret_access_key=self.config.aws_secret_access_key
            )
            
        except NoCredentialsError:
            raise AWSCredentialsError("AWS credentials illa!")
        except Exception as e:
            raise AWSCredentialsError(f"Client initialization fail: {e}")
    
    def _validate_image(self, image_path: str) -> None:
        """Image file validate"""
        if not os.path.exists(image_path):
            raise ImageNotFoundError(f"Image file illa: {image_path}")
        
        ext = os.path.splitext(image_path)[1].lower()
        if ext not in SUPPORTED_IMAGE_FORMATS:
            raise InvalidImageError(
                f"Invalid format: {ext}. Supported: {SUPPORTED_IMAGE_FORMATS}"
            )
        
        file_size_mb = os.path.getsize(image_path) / (1024 * 1024)
        if file_size_mb > 15:
            raise ImageTooLargeError(
                f"Image too large: {file_size_mb:.2f}MB. Max: 15MB"
            )
    
    def detect_labels(
        self,
        image_path: str,
        max_labels: Optional[int] = None,
        min_confidence: Optional[float] = None
    ) -> DetectionResult:
        """
        Detect labels in image
        
        Args:
            image_path: Local image file path
        
        Returns:
            DetectionResult with labels
        """
        result = DetectionResult(image_path=image_path)
        s3_key = ""
        
        try:
            self._validate_image(image_path)
            s3_key = self._s3_handler.upload_image(image_path)
            result.s3_key = s3_key
            
            response = self._rekognition_client.detect_labels(
                Image={
                    'S3Object': {
                        'Bucket': self.config.bucket_name,
                        'Name': s3_key
                    }
                },
                MaxLabels=max_labels or self.settings.max_labels,
                MinConfidence=min_confidence or self.settings.min_confidence
            )
            
            for label_data in response.get('Labels', []):
                parents = [p['Name'] for p in label_data.get('Parents', [])]
                
                label = Label(
                    name=label_data['Name'],
                    confidence=label_data['Confidence'],
                    parents=parents
                )
                result.labels.append(label)
            
            result.success = True
            
        except Exception as e:
            result.error_message = str(e)
            raise
            
        finally:
            if self.auto_cleanup and s3_key:
                try:
                    self._s3_handler.delete_image(s3_key)
                except Exception:
                    pass
        
        return result
    
    def detect_faces(self, image_path: str) -> Dict[str, Any]:
        """Detect faces in image"""
        s3_key = ""
        
        try:
            self._validate_image(image_path)
            s3_key = self._s3_handler.upload_image(image_path)
            
            response = self._rekognition_client.detect_faces(
                Image={
                    'S3Object': {
                        'Bucket': self.config.bucket_name,
                        'Name': s3_key
                    }
                },
                Attributes=['ALL']
            )
            
            return {
                'success': True,
                'face_count': len(response.get('FaceDetails', [])),
                'faces': response.get('FaceDetails', [])
            }
            
        finally:
            if self.auto_cleanup and s3_key:
                try:
                    self._s3_handler.delete_image(s3_key)
                except Exception:
                    pass
    
    def detect_text(self, image_path: str) -> Dict[str, Any]:
        """Detect text in image"""
        s3_key = ""
        
        try:
            self._validate_image(image_path)
            s3_key = self._s3_handler.upload_image(image_path)
            
            response = self._rekognition_client.detect_text(
                Image={
                    'S3Object': {
                        'Bucket': self.config.bucket_name,
                        'Name': s3_key
                    }
                }
            )
            
            texts = []
            for text in response.get('TextDetections', []):
                if text['Type'] == 'LINE':
                    texts.append({
                        'text': text['DetectedText'],
                        'confidence': text['Confidence']
                    })
            
            return {
                'success': True,
                'text_count': len(texts),
                'texts': texts
            }
            
        finally:
            if self.auto_cleanup and s3_key:
                try:
                    self._s3_handler.delete_image(s3_key)
                except Exception:
                    pass


# ============================================
# 🚀 SIMPLE FUNCTIONS - Users ku easy!
# ============================================

# Global client instance
_default_client = None

def _get_client() -> AWSRekognition:
    """Get or create default client"""
    global _default_client
    if _default_client is None:
        _default_client = AWSRekognition()
    return _default_client


def detect_labels(image_path: str, max_labels: int = 10, min_confidence: float = 75.0) -> DetectionResult:
    """
    Simple label detection - Just give image path!
    
    Usage:
        from aws_rekognition_tool import detect_labels
        
        result = detect_labels("/path/to/image.jpg")
        result.print_labels()
    """
    client = _get_client()
    return client.detect_labels(image_path, max_labels, min_confidence)


def detect_faces(image_path: str) -> Dict[str, Any]:
    """
    Simple face detection - Just give image path!
    
    Usage:
        from aws_rekognition_tool import detect_faces
        
        result = detect_faces("/path/to/photo.jpg")
        print(f"Faces found: {result['face_count']}")
    """
    client = _get_client()
    return client.detect_faces(image_path)


def detect_text(image_path: str) -> Dict[str, Any]:
    """
    Simple text detection - Just give image path!
    
    Usage:
        from aws_rekognition_tool import detect_text
        
        result = detect_text("/path/to/document.jpg")
        for text in result['texts']:
            print(text['text'])
    """
    client = _get_client()
    return client.detect_text(image_path)


def analyze_image(image_path: str) -> Dict[str, Any]:
    """
    Complete image analysis - Labels, faces, text
    
    Usage:
        from aws_rekognition_tool import analyze_image
        
        result = analyze_image("/path/to/image.jpg")
        print(result)
    """
    return {
        'labels': detect_labels(image_path).to_dict(),
        'faces': detect_faces(image_path),
        'text': detect_text(image_path)
    }