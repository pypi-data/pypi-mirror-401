
"""
Serious time utilities for PromptScope.
Provides robust UTC time, ISO formatting, monotonic timing, and elapsed time helpers.
"""

import time as _time
from datetime import datetime, timezone, timedelta
from typing import Optional

def now_utc() -> datetime:
	"""
	Get the current UTC datetime (timezone-aware).
	Returns:
		datetime: Current UTC time (aware).
	"""
	return datetime.now(timezone.utc)

def now_iso() -> str:
	"""
	Get the current UTC time as an ISO 8601 string.
	Returns:
		str: ISO 8601 formatted UTC time.
	"""
	return now_utc().isoformat()

def parse_iso(dt_str: str) -> datetime:
	"""
	Parse an ISO 8601 datetime string to a timezone-aware datetime.
	Args:
		dt_str: ISO 8601 string.
	Returns:
		datetime: Parsed datetime (aware if possible).
	"""
	dt = datetime.fromisoformat(dt_str)
	if dt.tzinfo is None:
		return dt.replace(tzinfo=timezone.utc)
	return dt


def ensure_utc(dt: datetime) -> datetime:
	"""
	Normalize a datetime to UTC, making naive inputs explicitly UTC.
	"""
	if dt.tzinfo is None:
		return dt.replace(tzinfo=timezone.utc)
	return dt.astimezone(timezone.utc)


def to_timestamp(dt: datetime) -> float:
	"""
	Convert a datetime to seconds since epoch (UTC).
	"""
	return ensure_utc(dt).timestamp()


def from_timestamp(ts: float) -> datetime:
	"""
	Convert epoch seconds to a timezone-aware UTC datetime.
	"""
	return datetime.fromtimestamp(ts, tz=timezone.utc)

def monotonic() -> float:
	"""
	Get a monotonic clock value (seconds, never goes backward).
	Returns:
		float: Monotonic time in seconds.
	"""
	return _time.monotonic()

def elapsed(start: float, end: Optional[float] = None) -> float:
	"""
	Compute elapsed time in seconds from start to end (monotonic).
	Args:
		start: Start time (from monotonic()).
		end: End time (from monotonic()), or now if None.
	Returns:
		float: Elapsed seconds.
	"""
	if end is None:
		end = monotonic()
	return end - start

def sleep(seconds: float):
	"""
	Sleep for the given number of seconds (wrapper for time.sleep).
	Args:
		seconds: Number of seconds to sleep.
	"""
	_time.sleep(seconds)
