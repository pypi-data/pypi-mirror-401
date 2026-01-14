# AWS Rekognition Tool 🔍

Easy-to-use Python package for AWS Rekognition - Detect labels, faces, and text in images!

## Installation

```bash
pip install aws-rekognition-tool



from aws_rekognition_tool import detect_labels
LOCAL_IMAGE_PATH = "/home/devel-balamurugan/adv3.png" 
 
 
result = detect_labels(LOCAL_IMAGE_PATH)
print(f"==>> result: {result}")