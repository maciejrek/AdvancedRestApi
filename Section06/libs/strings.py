"""
libs.strings

By defaut, uses 'en-gb.json' file inside the 'strings' top-level folder.

If language changes, set 'libs.strings.default_locale'
and run 'libs.strings.refresh()'
"""

import json

default_locale = "en-gb"
cached_strings = {}


def refresh():
    global cached_strings
    with open(f"strings/{default_locale}.json") as f:
        cached_strings = json.load(f)


def gettext(name: str):
    return cached_strings[name]


# We can add setter to change default_locale
# def set_default_locale(locale):
#     global default_locale
#     default_locale = locale
# Otherwise to change locale we need to:
# import strings
# strings.default_locale = "new-locale"
# strings.refresh()

refresh()
