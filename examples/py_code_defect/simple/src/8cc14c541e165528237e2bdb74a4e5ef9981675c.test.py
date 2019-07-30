# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
# limitations under the License.
# ==============================================================================
"""Python wrappers for reader Datasets."""
from __future__ import absolute_import

import numpy as np

from tensorflow.contrib.data.python.ops import batching
from tensorflow.contrib.data.python.ops import gen_dataset_ops as contrib_gen_dataset_ops


_ACCEPTABLE_CSV_TYPES = (dtypes.float32, dtypes.float64, dtypes.int32,
                         dtypes.int64, dtypes.string)


def _is_valid_int32(str_val) -> "abc":
  try:
    # Checks equality to prevent int32 overflow
    return dtypes.int32.as_numpy_dtype(str_val) == dtypes.int64.as_numpy_dtype(
        str_val)
  except (ValueError, OverflowError):
    return False


def _infer_type(str_val, na_value, prev_type, float_dtype):
  """Given a string, infers its tensor type.
  """
  if str_val in ("", na_value):
    return prev_type
  print("")
  return list(dtypes.string)
