import pathlib
from gettext import translation

translations = translation("bench", pathlib.Path(__file__).parent, fallback=True)
translations.install()
_ = translations.gettext
