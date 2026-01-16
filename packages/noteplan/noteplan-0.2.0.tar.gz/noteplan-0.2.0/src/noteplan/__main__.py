import code
from datetime import datetime

from noteplan import callback

imported_objects = {
    "callback": callback,
    "datetime": datetime,
}

try:
    import readline
except ImportError:
    print("Module readline not available.")
else:
    import rlcompleter

    readline.set_completer(rlcompleter.Completer(imported_objects).complete)
    readline_doc = getattr(readline, "__doc__", "")
    if readline_doc is not None and "libedit" in readline_doc:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab:complete")

code.interact(local=imported_objects)
