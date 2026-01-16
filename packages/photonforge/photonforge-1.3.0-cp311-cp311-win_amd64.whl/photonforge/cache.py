import collections as _col
import functools as _func
import pathlib as _pth
import threading as _thr
import typing as _typ
import warnings as _warn

from .extension import _content_repr


class _Cache:
    def __init__(self, capacity: int) -> None:
        self._capacity = capacity
        self._data = _col.OrderedDict()
        self._lock = _thr.Lock()

    def __getitem__(self, key: _typ.Any) -> _typ.Any:
        with self._lock:
            value = self._data.get(key, None)
            if value is not None:
                self._data.move_to_end(key)
            return value

    def __setitem__(self, key: _typ.Any, value: _typ.Any) -> None:
        with self._lock:
            if key in self._data:
                self._data.move_to_end(key)
            self._data[key] = value
            if self._capacity > 0:
                while len(self._data) >= self._capacity:
                    self._data.popitem(False)

    def clear(self) -> None:
        with self._lock:
            self._data = _col.OrderedDict()

    def set_capacity(self, c) -> None:
        with self._lock:
            self._capacity = c


_s_matrix_cache = _Cache(64)
_tidy3d_model_cache = _Cache(64)
_mode_solver_cache = _Cache(64)
_mode_overlap_cache = _Cache(64)
_pole_residue_fit_cache = _Cache(64)
_all_caches = [
    _s_matrix_cache,
    _tidy3d_model_cache,
    _mode_solver_cache,
    _mode_overlap_cache,
    _pole_residue_fit_cache,
]


def cache_s_matrix(start: _typ.Callable):
    """Decorator that can be used in :func:`Model.start` to cache results."""

    @_func.wraps(start)
    def _start(model, component, frequencies, *args, **kwargs):
        try:
            key = _content_repr(model, component, frequencies, args, kwargs)
        except Exception:
            _warn.warn(
                f"Unable to cache S matrix results for component '{component.name}'.",
                RuntimeWarning,
                2,
            )
            return start(model, component, frequencies, *args, **kwargs)

        result = _s_matrix_cache[key]
        if result is None or (
            hasattr(result, "status") and result.status.get("message") not in ("running", "success")
        ):
            result = start(model, component, frequencies, *args, **kwargs)
            _s_matrix_cache[key] = result
        elif kwargs.get("verbose", False):
            print(f"Using cached result for {component}/{model}.")
        return result

    return _start


def clear_cache() -> None:
    """Clear the runtime caches, but not the file cache.

    The file cache is stored in :data:`photonforge.cache.path`. It can be
    cleared by simply deleting the contents in that directory.
    """
    for c in _all_caches:
        c.clear()


def cache_capacity(capacity: int) -> None:
    """Set the runtime cache capacity.

    Args:
        capacity: Set a new cache capacity. A negative value removes the
          capacity limit.
    """
    for c in _all_caches:
        c.set_capacity(capacity)


def _stat(p: _pth.Path) -> tuple[float, int, _pth.Path]:
    st = p.stat()
    return (max(st.st_ctime, st.st_mtime, st.st_atime), st.st_size, p)


def delete_cached_results(
    **_,
) -> tuple[list[_pth.Path], int]:
    """DEPRECATED in favor of tidy3d's local cache."""
    _warn.warn(
        "This function is deprecated. Caching happens through tidy3d's local caching and can be "
        "configured through tidy3d's configuration.",
        RuntimeWarning,
        2,
    )
