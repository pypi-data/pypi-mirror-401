from datetime import datetime
from urllib.parse import urlencode

from . import convert


# https://help.noteplan.co/article/49-x-callback-url-scheme
def callback(action: str, parameters: dict) -> str:
    return f"noteplan://x-callback-url/{action}?{urlencode(parameters)}"


def open_note(*, noteDate: str | datetime | None = None, **parameters):
    match noteDate:
        case str():
            parameters.setdefault("noteDate", noteDate)
        case datetime():
            parameters.setdefault("noteDate", convert.day(noteDate))
    return callback("openNote", parameters)
