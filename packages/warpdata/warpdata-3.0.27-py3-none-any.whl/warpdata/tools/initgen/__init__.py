"""Init generator for warpdata.

Generates runnable Python loaders tailored to datasets.
"""

from warpdata.tools.initgen.analyze import (
    analyze_manifest,
    ManifestAnalysis,
    TableAnalysis,
    BindingInfo,
)
from warpdata.tools.initgen.generator import (
    LoaderGenerator,
    generate_loader,
)
from warpdata.tools.initgen.naming import (
    dataset_id_to_filename,
    dataset_id_to_module_name,
    column_to_function_name,
)

__all__ = [
    "analyze_manifest",
    "ManifestAnalysis",
    "TableAnalysis",
    "BindingInfo",
    "LoaderGenerator",
    "generate_loader",
    "dataset_id_to_filename",
    "dataset_id_to_module_name",
    "column_to_function_name",
]
