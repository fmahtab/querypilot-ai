import boto3
from pathlib import Path

REGION = "us-east-2"
BUCKET = "querypilot-docs-fm-2026"
LOCAL_DIR = Path("data/retailstar_docs")
PREFIX = "retailstar_docs/"  # acts like a folder inside the bucket

s3 = boto3.client("s3", region_name=REGION)

for file in LOCAL_DIR.glob("*.md"):
    key = PREFIX + file.name
    s3.upload_file(
        str(file), BUCKET, key,
        ExtraArgs={"ContentType": "text/markdown"},
    )
    print(f"Uploaded {file.name} -> s3://{BUCKET}/{key}")

# Confirm what's in the bucket
resp = s3.list_objects_v2(Bucket=BUCKET, Prefix=PREFIX)
print(f"\n{resp['KeyCount']} files in bucket:")
for obj in resp.get("Contents", []):
    print(f" - {obj['Key']} ({obj['Size']} bytes)")