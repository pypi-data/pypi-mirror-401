"""Utilities."""

from __future__ import annotations

from datetime import UTC, datetime
from functools import partial
from typing import Any


class Entries(list):
    """A list of entries with utility methods."""

    def __str__(self) -> str:
        return f"Entries({super().__str__()})"

    def __repr__(self) -> str:
        return f"Entries({super().__repr__()})"

    def newest(self: list[dict], key: str = "created_at") -> Entry:
        """Return the newest entry."""
        if not self:
            msg = "Cannot get newest entry from an empty list."
            raise ValueError(msg)
        return Entry(max(self, key=partial(_parse_created_at, key=key)))

    def oldest(self: list[dict], key: str = "created_at") -> Entry:
        """Return the oldest entry."""
        if not self:
            msg = "Cannot get oldest entry from an empty list."
            raise ValueError(msg)
        return Entry(min(self, key=partial(_parse_created_at, key=key)))

    def groupby(self, *tags: str) -> dict[str | tuple[str, ...], Entries]:
        """Group entries by one or more tag values.

        Args:
            tags: the tags to group by.

        Returns:
            A dictionary where the keys are tag values (or tuples of tag values
            for multiple tags) and the values are lists of entries that have
            those tags.
        """
        grouped: dict[str | tuple[str, ...], Entries] = {}
        for entry in self:
            key_parts = []
            skip = False
            for t in tags:
                props = entry["tags"].get(t)
                if props is None:
                    skip = True
                    break
                value = props["parameter_value"]
                key_parts.append(f"{t}:{value}")
            if skip:
                continue
            key: str | tuple[str, ...] = (
                key_parts[0] if len(key_parts) == 1 else tuple(key_parts)
            )
            if key not in grouped:
                grouped[key] = Entries()
            grouped[key].append(entry)
        return grouped

    def __getitem__(self, index: Any) -> Any:
        """Get an entry by index."""
        try:
            return Entry(super().__getitem__(index))
        except Exception:  # noqa: BLE001
            return super().__getitem__(index)


class Entry(dict):
    """A dictionary representing an entry with utility methods."""

    def __str__(self) -> str:
        return f"Entry({super().__str__()})"

    def __repr__(self) -> str:
        return f"Entry({super().__repr__()})"

    def __getattr__(self, key: str) -> Any:
        """Get an attribute from the entry."""
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(str(e)) from e


def _parse_created_at(entry: dict, *, key: str) -> datetime:
    """Parse the created_at field from an entry.

    Returns the Unix epoch start if the field is missing or can't be parsed.
    """
    try:
        created_at_str = entry.get(key)
        if not created_at_str:
            return datetime.fromtimestamp(0, tz=UTC)
        return datetime.fromisoformat(created_at_str)
    except (ValueError, TypeError):
        return datetime.fromtimestamp(0, tz=UTC)
