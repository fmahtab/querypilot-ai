import boto3

REGION = "us-east-2"
BUCKET = "querypilot-docs-fm-2026"  # must be unique across ALL of AWS

s3 = boto3.client("s3", region_name=REGION)

# 1. Create the bucket
s3.create_bucket(
    Bucket=BUCKET,
    CreateBucketConfiguration={"LocationConstraint": REGION},
)
print(f"Created bucket: {BUCKET}")

# 2. List all your buckets
for b in s3.list_buckets()["Buckets"]:
    print(" -", b["Name"])