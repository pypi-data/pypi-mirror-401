# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from __future__ import annotations

import io
import logging
from collections.abc import Callable
from typing import Any

import geneva
import pyarrow as pa
from pybase64 import b64decode

_LOG = logging.getLogger(__name__)

MODEL_ID = "google/vit-base-patch16-224"
IMAGE_SIZE = 224
_PIXEL_VALUES_LEN = 3 * IMAGE_SIZE * IMAGE_SIZE

_DECODED_STRUCT = pa.struct(
    [
        pa.field("image_bytes", pa.large_binary()),
        pa.field("width", pa.int32()),
        pa.field("height", pa.int32()),
    ]
)

_PREPROCESSED_TYPE = pa.list_(pa.float32(), _PIXEL_VALUES_LEN)

_PROCESSOR = None


def _get_processor():  # noqa: ANN202
    global _PROCESSOR  # noqa: PLW0603
    if _PROCESSOR is None:
        from transformers import ViTImageProcessor

        _PROCESSOR = ViTImageProcessor(
            do_convert_rgb=None,
            do_normalize=True,
            do_rescale=True,
            do_resize=True,
            image_mean=[0.5, 0.5, 0.5],
            image_std=[0.5, 0.5, 0.5],
            resample=2,
            rescale_factor=0.00392156862745098,
            size={"height": IMAGE_SIZE, "width": IMAGE_SIZE},
        )
    return _PROCESSOR


@geneva.udf(version="0.1", data_type=_DECODED_STRUCT)
def decode(image: bytes | None) -> dict[str, Any] | None:
    """
    Decode base64 image bytes and extract width/height.

    Geneva maps returned dicts to pa.struct fields.
    """
    if not image:
        return None
    try:
        decoded = b64decode(image, None, True)
        from PIL import Image

        img = Image.open(io.BytesIO(decoded))
        width, height = img.size
        return {
            "image_bytes": decoded,
            "width": int(width),
            "height": int(height),
        }
    except Exception as exc:  # pragma: no cover
        _LOG.warning("Failed to decode image payload: %s", exc)
        return None


@geneva.udf(version="0.1", data_type=_PREPROCESSED_TYPE)
def preprocess(decoded: dict[str, Any] | None):  # noqa: ANN202
    if not decoded:
        return None

    image_bytes = decoded.get("image_bytes")
    if not image_bytes:
        return None

    try:
        import numpy as np
        from PIL import Image

        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        outputs = _get_processor()(images=img)["pixel_values"]
        if len(outputs) != 1:  # pragma: no cover
            raise ValueError(f"Expected 1 image output, got {len(outputs)}")

        return np.asarray(outputs[0], dtype=np.float32).reshape(-1)
    except Exception as exc:  # pragma: no cover
        _LOG.warning("Failed to preprocess image payload: %s", exc)
        return None


@geneva.udf(version="0.1", data_type=pa.list_(pa.float32(), 1000))
class Infer(Callable):
    def __init__(self) -> None:
        self._model = None
        self._device = None

    def setup(self) -> None:
        import torch
        from transformers import ViTForImageClassification

        self._device = "cuda" if torch.cuda.is_available() else "cpu"
        self._model = ViTForImageClassification.from_pretrained(
            MODEL_ID
        ).to(self._device)
        self._model.eval()

    def __call__(self, preprocessed: Any | None) -> list[float] | None:
        if preprocessed is None:
            return None

        if self._model is None or self._device is None:
            self.setup()

        import torch
        import numpy as np

        pixel_values = np.asarray(preprocessed, dtype=np.float32).reshape(
            (1, 3, IMAGE_SIZE, IMAGE_SIZE)
        )
        pixel_values = torch.from_numpy(pixel_values).to(
            dtype=torch.float32, device=self._device, non_blocking=True
        )

        with torch.inference_mode():
            logits = self._model(pixel_values=pixel_values).logits
        return logits.squeeze(0).cpu().tolist()


__all__ = ["Infer", "decode", "preprocess"]
