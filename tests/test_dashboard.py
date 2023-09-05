from dashboard import extract_info

def test_extract_info():
    dict_test = {'TEST_first': 0,
            'TEST_second': 1,
            'TEST_third': 0}
    dict_wrong = {'TEST_first': 0,
                  'TEST_second': 0,
                  'TEST_third': 0}
    assert extract_info(dict_test) == 'second'
    assert extract_info(dict_wrong) == None

