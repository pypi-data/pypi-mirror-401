"""WarpDatasets v3 - Remote-first dataset library for ML training."""

from warpdata.api.dataset import Dataset, dataset, from_manifest
from warpdata.config.backends import use_backblaze, use_s3
from warpdata import ingest
from warpdata import compat

__version__ = "3.0.27"
__all__ = [
    "dataset",
    "Dataset",
    "from_manifest",
    "ingest",
    "compat",
    "use_backblaze",
    "use_s3",
    "__version__",
]
