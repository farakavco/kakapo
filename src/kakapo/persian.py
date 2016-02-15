# -*- coding: utf-8 -*-
__author__ = 'vahid'
_character_map = {
    'ي': 'ی',
    'ك': 'ک',
    'ة': 'ه',
    'ۀ': 'ه',

    # Eastern Arabic-Indic digits (Persian and Urdu) U+06Fn: ۰۱۲۳۴۵۶۷۸۹
    '۰': '0',
    '۱': '1',
    '۲': '2',
    '۳': '3',
    '۴': '4',
    '۵': '5',
    '۶': '6',
    '۷': '7',
    '۸': '8',
    '۹': '9',


    # Arabic-Indic digits: U+066n: ٠١٢٣٤٥٦٧٨٩
    '٠': '0',
    '١': '1',
    '٢': '2',
    '٣': '3',
    '٤': '4',
    '٥': '5',
    '٦': '6',
    '٧': '7',
    '٨': '8',
    '٩': '9',

}


def purify(s):
    res = ''
    for c in s:
        if c in _character_map:
            res += _character_map[c]
        else:
            res += c
    return res


if __name__ == '__main__':
    sample_input = 'يكةۀ'
    expected_output = 'یکهه'

    assert purify(sample_input) == expected_output
    print('success')
