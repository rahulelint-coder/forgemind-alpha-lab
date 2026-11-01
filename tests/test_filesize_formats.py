import struct
import pytest
from humanize import naturalsize, i18n
CASES=[('literal-decimal-promotion', 999999, {'format': 'build2.7 %.1f'}, '.', 'build2.7 1.0 MB'), ('negative-literal-promotion', -999999, {'format': 'build2.7 %.1f'}, ',', 'build2.7 -1,0 MB'), ('binary-literal-promotion', 1048575, {'binary': True, 'format': 'build2.7 %.1f'}, ',', 'build2.7 1,0 MiB'), ('gnu-literal-promotion', 1048575, {'gnu': True, 'format': 'build2.7 %.1f'}, ',', 'build2.7 1,0M'), ('largest-suffix-literal', 10000000000000000000000000000000000, {'format': 'build2.7 %.1f'}, ',', 'build2.7 10000,0 QB'), ('scientific-literal', 1500000, {'format': 'rev3.8: %.2e'}, ',', 'rev3.8: 1,50e+00 MB'), ('escaped-percents', 3000, {'format': 'rev3.8 %% %.2f%%'}, ',', 'rev3.8 % 3,00% kB'), ('literal-suffix-control', 3000, {'format': '%.1f (rev3.8)'}, ',', '3,0 (rev3.8) kB'), ('sign-width-zero-padding', 3000, {'format': 'ref1.2 [%+08.2f]'}, ',', 'ref1.2 [+0003,00] kB'), ('left-padding', 3000, {'format': 'v4.2|%-7.2f|'}, ',', 'v4.2|3,00   | kB'), ('significant-rounding', 999999, {'format': '%.2g'}, ',', '1 MB'), ('integer-precision', 999999, {'format': 'rev1.3 %d'}, ',', 'rev1.3 999 kB'), ('string-conversion', 3000, {'format': 'rev1.3 %s'}, ',', 'rev1.3 3,0 kB'), ('small-bytes-control', 300, {}, ',', '300 Bytes'), ('negative-singular-control', -1, {}, ',', '-1 Byte'), ('negative-binary-control', -4096, {'binary': True}, '.', '-4.0 KiB'), ('general-percent', 3000, {'format': 'version1.0_%%_%g'}, ',', 'version1.0_%_3 kB'), ('multiple-literal-numbers', 3000, {'format': '1.0 build2.7 X%.3fY'}, ',', '1.0 build2.7 X3,000Y kB'), ('gnu-padding', 3000, {'gnu': True, 'format': '%05.1f'}, ',', '002,9K'), ('uppercase-scientific', 3000, {'format': 'rev2.1: %.1E'}, ',', 'rev2.1: 3,0E+00 kB'), ('ordinary-rounding-control', 999999, {}, '.', '1.0 MB'), ('bare-h-modifier', 3000, {'format': '%hf'}, '.', '3.000000 kB'), ('bare-l-modifier', 3000, {'format': '%lf'}, '.', '3.000000 kB'), ('bare-L-modifier', 3000, {'format': '%Lf'}, '.', '3.000000 kB'), ('literal-h-modifier', 3000, {'format': 'rev2.8 %hf'}, ',', 'rev2.8 3,000000 kB'), ('literal-l-modifier', 3000, {'format': 'rev2.8 %lf'}, ',', 'rev2.8 3,000000 kB'), ('literal-L-modifier', 3000, {'format': 'rev2.8 %Lf'}, ',', 'rev2.8 3,000000 kB'), ('integer-length-modifier', 3000, {'format': 'rev2.8 %ld'}, ',', 'rev2.8 3 kB'), ('padded-length-modifier', 3000, {'format': 'rev2.8 %+07.2lf'}, ',', 'rev2.8 +003,00 kB'), ('string-double-escaped-percent', 3000, {'format': '%s%%%%'}, '.', '3.0%% kB'), ('public-invalid-format-0', 3000, {'format': '%q'}, '.', {'raises': ['value_error', 'type_error']}), ('public-invalid-format-1', 3000, {'format': 'no conversion'}, '.', {'raises': ['value_error', 'type_error']}), ('public-invalid-format-2', 3000, {'format': '%%'}, '.', {'raises': ['value_error', 'type_error']}), ('public-invalid-format-3', 3000, {'format': '%*f'}, '.', {'raises': ['value_error', 'type_error']}), ('public-invalid-format-4', 3000, {'format': '%.1f %.1f'}, '.', {'raises': ['value_error', 'type_error']})]
@pytest.fixture(scope="module")
def public_test_locales(tmp_path_factory):
    root=tmp_path_factory.mktemp("filesize-locales")
    for locale in ("fr_FR","de_DE"):
        path=root/locale/"LC_MESSAGES"/"humanize.mo"
        path.parent.mkdir(parents=True)
        path.write_bytes(struct.pack("<7I",0x950412de,0,0,28,28,0,0))
    return root
@pytest.mark.parametrize("case",CASES,ids=[row[0] for row in CASES])
def test_public_compatibility(case,public_test_locales):
    name,value,kwargs,separator,expected=case
    i18n.deactivate()
    try:
        if separator==",": i18n.activate("fr_FR",path=public_test_locales)
        if isinstance(expected,dict):
            errors=tuple({"value_error":ValueError,"type_error":TypeError}[v] for v in expected["raises"])
            with pytest.raises(errors): naturalsize(value,**kwargs)
        else: assert naturalsize(value,**kwargs)==expected
    finally: i18n.deactivate()
def test_actual_locale_activation_switch_and_deactivation(public_test_locales):
    try:
        for locale,expected in (("fr_FR","release1.2 1,5 MB"),("de_DE","release1.2 1,5 MB"),("en_US","release1.2 1.5 MB")):
            i18n.activate(locale,path=public_test_locales)
            assert naturalsize(1500000,format="release1.2 %.1f")==expected
    finally: i18n.deactivate()
    assert naturalsize(1500000,format="release1.2 %.1f")=="release1.2 1.5 MB"
