from pathlib import Path
from app.services.rag.loader import load_all_markdown_files, load_all_markdown_from_s3

local = load_all_markdown_files(Path("data/retailstar_docs"))
cloud = load_all_markdown_from_s3("querypilot-docs-fm-2026", "retailstar_docs/")

print(f"Local: {len(local)} docs | S3: {len(cloud)} docs")
print("Identical:", local == cloud)

for (ln, lm, lb), (cn, cm, cb) in zip(local, cloud):
    if (ln, lm, lb) != (cn, cm, cb):
        print(f"\nDiffers: {ln}")
        print("  names match:   ", ln == cn)
        print("  metadata match:", lm == cm)
        print("  body match:    ", lb == cb)
        print("  \\r in S3 body: ", "\r" in cb)
        break