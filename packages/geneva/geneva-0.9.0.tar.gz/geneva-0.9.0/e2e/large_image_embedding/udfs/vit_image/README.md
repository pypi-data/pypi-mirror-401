# ViT Image UDF Package

UDFs for the large image embedding suite:

- `decoded`: decode base64 payloads and extract width/height (struct)
- `preprocessed`: ViT preprocessing (resize/rescale/normalize → 3x224x224 float32)
- `vit_logits`: run `google/vit-base-patch16-224` and return 1000-dim logits

Upload via:

```bash
export GENEVA_TABLE_NAME=my_table
uv run python upload_manifest.py --bucket gs://bucket/path
```
