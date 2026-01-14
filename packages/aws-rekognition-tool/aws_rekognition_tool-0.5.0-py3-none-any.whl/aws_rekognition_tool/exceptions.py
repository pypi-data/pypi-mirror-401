"""
Custom Exceptions - Namma package ku special errors
"""


class RekognitionToolError(Exception):
    """Base exception for all package errors"""
    pass


class AWSCredentialsError(RekognitionToolError):
    """AWS credentials illama irundha ithu raise aagum"""
    pass


class ImageNotFoundError(RekognitionToolError):
    """Local image file illa na ithu raise aagum"""
    pass


class S3UploadError(RekognitionToolError):
    """S3 upload fail aana ithu raise aagum"""
    pass


class S3DeleteError(RekognitionToolError):
    """S3 delete fail aana ithu raise aagum"""
    pass


class RekognitionError(RekognitionToolError):
    """Rekognition API fail aana ithu raise aagum"""
    pass


class InvalidImageError(RekognitionToolError):
    """Image format wrong ah irundha ithu raise aagum"""
    pass


class ImageTooLargeError(RekognitionToolError):
    """Image size perusa irundha ithu raise aagum"""
    pass