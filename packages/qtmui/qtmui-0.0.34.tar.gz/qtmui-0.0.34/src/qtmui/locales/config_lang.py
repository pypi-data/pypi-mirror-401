from functools import reduce
from copy import deepcopy

# Import các thành phần tương tự từ các tệp liên quan
from .langs.vi import vi
from .langs.en import en

# Hàm để merge dict tương tự lodash.merge
def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

# Hàm chính tương tự với 'componentsOverrides' trong JavaScript
allLangs = merge_dicts(
    vi,
    en,
)


defaultLang = allLangs["en"]