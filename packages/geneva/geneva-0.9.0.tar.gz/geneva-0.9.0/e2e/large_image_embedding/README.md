# Large Image Embedding E2E Suite

End-to-end tests for running a base64-image decoding + ViT inference pipeline on
Geneva. This suite is adapted from Ray's nightly benchmark: [large_image_embedding](https://github.com/ray-project/ray/tree/master/release/nightly_tests/multimodal_inference_benchmarks/large_image_embedding).

## Pipeline (Geneva)

1. Decode base64 image bytes and extract width/height → `decoded` (pa.struct)
2. ViT preprocessing (resize/rescale/normalize) → `preprocessed` (3x224x224 float32)
3. Run ViT inference → `vit_logits` (1000-dim)

All heavy ML deps live in `udfs/vit_image` and are uploaded as a manifest
`large-image-embedding-udfs-v1`.

## Running Tests

From the workspace root:

```bash
uv sync --all-groups --all-extras --locked
make test-e2e-large-image-embedding-gcp SLUG=myrun NUM_LARGE_IMAGES=20 BATCH_SIZE=4
```

Or directly from the suite directory:

```bash
cd e2e/large_image_embedding
RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 uv run -m pytest test_drivers \
  --csp=gcp --num-images=20 --batch-size=4 -v
```
