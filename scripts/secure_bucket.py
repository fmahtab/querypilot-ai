import boto3

REGION = "us-east-2"
BUCKET = "querypilot-docs-fm-2026"

s3 = boto3.client("s3", region_name=REGION)

# 1. Turn on versioning
s3.put_bucket_versioning(
    Bucket=BUCKET,
    VersioningConfiguration={"Status": "Enabled"},
)
print("Versioning:", s3.get_bucket_versioning(Bucket=BUCKET).get("Status"))

# 2. Check encryption (S3 turns on SSE-S3 by default)
enc = s3.get_bucket_encryption(Bucket=BUCKET)
rule = enc["ServerSideEncryptionConfiguration"]["Rules"][0]
print("Encryption:", rule["ApplyServerSideEncryptionByDefault"]["SSEAlgorithm"])

# 3. Check public access is blocked
pab = s3.get_public_access_block(Bucket=BUCKET)["PublicAccessBlockConfiguration"]
print("Public access fully blocked:", all(pab.values()))