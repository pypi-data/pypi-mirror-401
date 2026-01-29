"""Typed reference objects for raw data access.

Provides FileRef, ImageRef, AudioRef for lazy, remote-first raw data access.
"""

from warpdata.refs.base import FileRef
from warpdata.refs.image import ImageRef
from warpdata.refs.audio import AudioRef
from warpdata.refs.factory import create_ref

__all__ = ["FileRef", "ImageRef", "AudioRef", "create_ref"]
