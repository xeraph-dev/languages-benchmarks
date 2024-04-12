import pathlib
from gettext import translation

translations = translation("bench", pathlib.Path(__file__).parent)
translations.install()
_ = translations.gettext
