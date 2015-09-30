from edttools import extract

def test_extract_infos():
    assert(extract.parse_infos("13:15-14:30,F1,S=FA106") == ((13, 15), (14, 30), 1, "FA106"))
    assert(extract.parse_infos(" 8:00- 9:00,F2,S=FA405") == ((8, 0), (9, 0), 2, "FA405"))
    assert(extract.parse_infos(" 9:00-13:00,F1,S=RI207") == ((9, 0), (13, 0), 1, "RI207"))

def test_extract_items():
    pass

