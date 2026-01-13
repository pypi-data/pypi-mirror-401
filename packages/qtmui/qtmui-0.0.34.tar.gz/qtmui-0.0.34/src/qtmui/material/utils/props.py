
from ..qss_name import *

dic__ = {
    my: "long"
}
print(dic__.get(my))

def list_to_multi_line_str(qss_list):
    qss_str = ""
    for item in qss_list:
        qss_str += f"{item}\n"
    return qss_str

def get_qss_from_sx(sx: dict):
    qss = []
    if sx.get("px") is not None:
        qss.append(sx.get("px")) # in px
    if sx.get("px") is not None:
        qss.append(sx.get("py")) # in py

    qss_str = list_to_multi_line_str(qss)
    return qss_str

