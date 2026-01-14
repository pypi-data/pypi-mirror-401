from aws_rekognition_tool import AWSRekognition

# Initialize
rekognition = AWSRekognition(
    aws_access_key_id="AKIAWB2BR3JONLL46PLZ",
    aws_secret_access_key="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",
    bucket_name="aidermatologistsnew",
    region_name="us-east-1"
)

# Detect labels in an image
result = rekognition.detect_labels("/home/devel-balamurugan/adv3.png" )
print(f"==>> result: {result}")

# Print results
result.print_labels()

# Access labels programmatically
for label in result.labels:
    print(f"{label.name}: {label.confidence:.2f}%")