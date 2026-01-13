from __future__ import annotations

import json
from typing import TYPE_CHECKING

from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST

from cartouche.compiler import update_translation

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@require_POST
def save(request: HttpRequest) -> HttpResponse:
    if not settings.DEBUG:
        return HttpResponseForbidden()

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError as e:
        return JsonResponse({"ok": False, "error": f"Invalid JSON: {e}"}, status=400)

    msgid = data.get("msgid")
    msgstr = data.get("msgstr")
    locale = data.get("locale")
    ctx = data.get("ctx")

    # Check required fields exist
    if msgid is None or msgstr is None or locale is None:
        return JsonResponse(
            {"ok": False, "error": "Missing required fields: msgid, msgstr, locale"},
            status=400,
        )

    try:
        po_path = update_translation(
            msgid=msgid,
            new_msgstr=msgstr,
            locale=locale,
            context=ctx,
        )
    except RuntimeError as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)

    if po_path:
        return JsonResponse({"ok": True, "file": str(po_path)})
    return JsonResponse({"ok": False, "error": "msgid not found"}, status=404)
