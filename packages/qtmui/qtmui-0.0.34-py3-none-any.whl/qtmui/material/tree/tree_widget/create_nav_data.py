def create_nav_data(data):
    # Khởi tạo cấu trúc kết quả với subheader
    result = [{
        'subheader': 'Members',
        'items': []
    }]
    
    # Tạo từ điển để theo dõi các node đã xử lý
    nodes = {}
    
    # Tạo tất cả các node và thêm vào dictionary nodes
    for item in data:
        node = {
            'title': item['title'],
            "parent_department": item['parent'],
            'path': '#',
            'icon': 'None',
            'id': item['id'],
            'onActionButtonClicked': 'None',
            'children': []
        }
        nodes[item['id']] = node

    # Thêm các node vào cây theo thứ tự parent-child
    for item in data:
        node = nodes[item['id']]
        if item['parent'] is None:
            result[0]['items'].append(node)
        else:
            parent_node = nodes.get(item['parent'])
            if parent_node:
                parent_node['children'].append(node)
    
    return result