import gettext
import pytest
from humanize import naturalsize, i18n

@pytest.mark.parametrize("locale", ["fr_FR", "de_DE"])
def test_naturalsize_respects_locale_decimal_separator(monkeypatch, locale):
 # Synthetic translation object avoids depending on unbuilt .mo artifacts.
 # The actual locale activation and decimal_separator logic are exercised.
 monkeypatch.setattr(i18n.gettext_module, "translation", lambda *a, **k: gettext.NullTranslations())
 i18n.activate(locale)
 try:
  assert i18n.decimal_separator() == ","
  assert naturalsize(1500000) == "1,5 MB"
 finally:
  i18n.deactivate()
