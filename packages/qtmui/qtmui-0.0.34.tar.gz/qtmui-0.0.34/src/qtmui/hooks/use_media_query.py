import re

def useMediaQuery(query: str, current_width: int = 1024, current_height: int = 768) -> bool:
    """
    Giả lập hook useMediaQuery trong React.
    
    Args:
        query (str): Chuỗi media query theo định dạng CSS, ví dụ:
            "(min-width: 800px)"
            "(max-width: 1200px)"
            "(min-width: 600px) and (max-width: 1200px)"
        current_width (int, optional): Chiều rộng hiện tại của cửa sổ hoặc môi trường. Mặc định là 1024.
        current_height (int, optional): Chiều cao hiện tại của cửa sổ hoặc môi trường. Mặc định là 768.
    
    Returns:
        bool: True nếu điều kiện của media query được thỏa mãn, ngược lại trả về False.
    
    Ví dụ:
        >>> use_media_query("(min-width: 800px)", current_width=1024)
        True
        >>> use_media_query("(max-width: 800px)", current_width=1024)
        False
        >>> use_media_query("(min-width: 600px) and (max-width: 1200px)", current_width=1024)
        True
    """
    # Tìm giá trị min-width và max-width thông qua regex
    min_width = None
    max_width = None

    # Regex tìm min-width và max-width, cho phép có khoảng trắng
    pattern_min = r"min-width\s*:\s*(\d+)"
    pattern_max = r"max-width\s*:\s*(\d+)"

    match_min = re.search(pattern_min, query)
    if match_min:
        min_width = int(match_min.group(1))

    match_max = re.search(pattern_max, query)
    if match_max:
        max_width = int(match_max.group(1))

    # Đánh giá điều kiện dựa trên kích thước hiện tại
    if min_width is not None and max_width is not None:
        return current_width >= min_width and current_width <= max_width
    elif min_width is not None:
        return current_width >= min_width
    elif max_width is not None:
        return current_width <= max_width
    else:
        # Nếu không có điều kiện nào được nhận diện, trả về False
        return False


# # Ví dụ sử dụng:
# if __name__ == "__main__":
#     test_queries = [
#         "(min-width: 800px)",
#         "(max-width: 1200px)",
#         "(min-width: 600px) and (max-width: 1200px)",
#         "(min-width: 1300px)"
#     ]

#     for q in test_queries:
#         result = use_media_query(q, current_width=1024)
#         print(f"Query: {q} -> {result}")
