from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import polib
from django.apps import apps
from django.conf import settings
from django.core.management import call_command

if TYPE_CHECKING:
    from collections.abc import Iterator


def find_po_entry(
    msgid: str,
    locale: str,
    context: str | None = None,
) -> tuple[Path, polib.POFile, polib.POEntry] | None:
    """Returns (po_path, po_file, entry) or None if not found."""
    for locale_dir in _locale_dirs():
        po_path = locale_dir / locale / "LC_MESSAGES" / "django.po"
        if not po_path.exists():
            continue
        try:
            po = polib.pofile(str(po_path))
        except OSError:
            continue
        entry = po.find(msgid, msgctxt=context)
        if entry:
            return po_path, po, entry
    return None


def update_translation(
    msgid: str,
    new_msgstr: str,
    locale: str,
    context: str | None = None,
) -> Path | None:
    """Returns .po path on success, None if msgid not found."""
    result = find_po_entry(msgid, locale, context)
    if not result:
        return None

    po_path, po, entry = result
    entry.msgstr = new_msgstr
    if "fuzzy" in entry.flags:
        entry.flags.remove("fuzzy")
    po.save()

    try:
        call_command("compilemessages", locale=[locale], verbosity=0)
    except Exception as e:
        raise RuntimeError(f"compilemessages failed: {e}") from e

    # Django's autoreload watches .mo files and clears translation caches
    # automatically (see django/utils/translation/reloader.py)
    return po_path


def _locale_dirs() -> Iterator[Path]:
    yield from (Path(p) for p in getattr(settings, "LOCALE_PATHS", []))
    for config in apps.get_app_configs():
        app_locale = Path(config.path) / "locale"
        if app_locale.is_dir():
            yield app_locale
