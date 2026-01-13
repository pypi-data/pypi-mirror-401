"""functional_list.backend

Backend implementations for ListMapper.

Public API:
- BaseBackend, BackendError
- SerialBackend
- LocalBackend
- AsyncBackend
- RayBackend (optional dependency: ray)
- DaskBackend (optional dependency: dask)
"""

from functional_list.backend.async_backend import AsyncBackend
from functional_list.backend.base import BackendError, BaseBackend
from functional_list.backend.dask_backend import DaskBackend
from functional_list.backend.local import LocalBackend
from functional_list.backend.ray_backend import RayBackend
from functional_list.backend.serial import SerialBackend

_BACKEND_EXPORTS = (
    "BaseBackend",
    "BackendError",
    "SerialBackend",
    "LocalBackend",
    "AsyncBackend",
    "RayBackend",
    "DaskBackend",
)

__all__ = list(_BACKEND_EXPORTS)
