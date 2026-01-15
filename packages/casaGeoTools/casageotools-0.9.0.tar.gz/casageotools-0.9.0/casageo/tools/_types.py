import datetime
import functools
import uuid
from typing import Self

from . import _util


class CasaGeoResult:
    def __init__(self, *, _data: dict, _error: Exception | None = None) -> None:
        self._timestamp = datetime.datetime.now()
        self._uuid = uuid.uuid4()
        self._data = _data
        self._error = _error

    def __bool__(self) -> bool:
        return self._error is None

    def __repr__(self) -> str:
        classname = type(self).__qualname__
        return f"<{classname} {self._uuid} [{'OK' if self else repr(self._error)}]>"

    @classmethod
    def from_response(cls, response: _util.Response) -> Self:
        # NOTE: If load_json() raises an exception, it will be caught by the
        #       decorator surrounding the calling function (if any).
        return cls(_data=_util.load_json(response))

    @classmethod
    def from_exception(cls, exception: Exception) -> Self:
        return cls(_data={}, _error=exception)

    @classmethod
    def wrap_errors(cls):
        """
        Decorator that wraps a function in a try-except block and returns any caught
        exception wrapped in a ``cls`` object.
        """

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    _util.logger.warning("%s: %s", err.__class__.__name__, err)
                    return cls.from_exception(err)

            return wrapper

        return decorator

    def json(self) -> dict:
        """
        Return the raw API response as a dictionary.

        Returns:
            dict: The raw JSON API response.
        """
        return self._data

    def error(self) -> Exception | None:
        """
        Return the exception that occurred during the API request, if any.

        Returns:
            Exception | None: The exception that occurred, or None if no exception occurred.
        """
        return self._error
