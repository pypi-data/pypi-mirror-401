from operator import attrgetter

def orderBy(data: list, fields, orders):
    """
    Sắp xếp danh sách các đối tượng theo các trường và thứ tự tương ứng.
    
    :param data: List các đối tượng cần sắp xếp.
    :param fields: Danh sách các tên thuộc tính của đối tượng để sắp xếp.
    :param orders: Danh sách các thứ tự sắp xếp tương ứng ('asc' hoặc 'desc').
    :return: Danh sách đã được sắp xếp.
    """
    if not fields or not orders or len(fields) != len(orders):
        raise ValueError("fields và orders phải có cùng độ dài và không được rỗng")
    
    sort_keys = [(field, reverse) for field, reverse in zip(fields, [o == "desc" for o in orders])]
    
    for field, reverse in reversed(sort_keys):
        data.sort(key=attrgetter(field), reverse=reverse)
    
    return data