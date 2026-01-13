from typing import Tuple, Union, Dict, List
from urllib.parse import parse_qs

class RouterParse():
    def __init__(self, list_router: List[dict]):
        self.map_all_route:list = list_router

    def paire_route(self,route:str="dashboard/user"):
        paire_routes = []
        if "/" in route:
            routes = route.split("/")
            for i in routes:
                if i == "":
                    continue
                paire_routes.append(i)
        else:
            paire_routes = [route]
        return paire_routes
    
    def get_dict_route(self,main_path:str="dashboard"):
        for route in self.map_all_route:
            path = route.get("path")
            if path == main_path:
                return route
        return {}
    
    def get_index_true(self,children:list=[]):
        for child in children:
            if child.get("index") == True:
                return child
        return {}
    
    def get_current_route(self,chilren:list=[], path:str=""):
        for route in chilren:
            if route.get("path") == path:
                return route
        return {}
    
    def extract_param_and_clean_path(self, path: str):
        """
        Hàm nhận một đường dẫn có chứa segment với dấu ':' và trả về:
        - Giá trị của segment đó (sau khi loại bỏ dấu ':')
        - Đường dẫn mới, loại bỏ segment chứa dấu ':'
        
        Ví dụ:
        Input: "/dashboard/user/:5/edit"
        Output: ("5", "/dashboard/user/edit")
        
        Input: "/dashboard/user/edit/:5"
        Output: ("5", "/dashboard/user/edit")
        """
        param = None

        if path.startswith("push//:"):
            path = path.split(':')
            new_path = path[1]
            param = path[0]
            path_and_params = new_path.split('?')
            new_path = path_and_params[0]
            param = path_and_params[1]
            # param=params.split("&&")
            return param, new_path
        
        elif path.startswith("replace//:"):
            path = path.split(':')
            new_path = path[1]
            param = path[0]
            return param, new_path

        elif path.find("/?") != -1:
            path = path.split('/?')
            new_path = path[0]
            param = path[1]
            return param, new_path

        segments = path.split('/')
        
        new_segments = []
        
        for seg in segments:
            if ':' in seg:
                # Lấy phần sau dấu ':' (có thể là toàn bộ chuỗi sau khi loại bỏ dấu ':')
                param = seg.replace(":", "")
            else:
                new_segments.append(seg)
        
        # Ghép lại các segment thành đường dẫn mới
        new_path = "/".join(new_segments)
        # Nếu đường dẫn ban đầu bắt đầu bằng '/', đảm bảo kết quả cũng bắt đầu bằng '/'
        if path.startswith("/") and not new_path.startswith("/"):
            new_path = "/" + new_path

        return param, new_path

    def extract_param_and_clean_path_new(self, path: str) -> Tuple[Union[str, Dict, None], str]:
        """
        Hàm nhận một đường dẫn và trả về:
        - Giá trị tham số (chuỗi nếu là :param, dictionary nếu là query string, hoặc None)
        - Đường dẫn mới, loại bỏ segment chứa :param hoặc query string
        
        Ví dụ:
        Input: "/dashboard/user/:5/edit"
        Output: ("5", "/dashboard/user/edit")
        
        Input: "/dashboard/user/edit?userName=6&password=4"
        Output: ({"userName": "6", "password": "4"}, "/dashboard/user/edit")
        
        Input: "/dashboard/user/edit"
        Output: (None, "/dashboard/user/edit")
        """
        param = None
        new_path = path

        # Xử lý query string (?key=value)
        if '?' in path:
            path_parts = path.split('?', 1)
            new_path = path_parts[0]  # Phần path trước query string
            query_string = path_parts[1] if len(path_parts) > 1 else ""
            
            # # Phân tích query string thành dictionary
            # if query_string:
            #     # parse_qs trả về dict với value là list (vì query string có thể lặp key)
            #     param_dict = parse_qs(query_string)
            #     # Chuyển value từ list sang single value nếu chỉ có 1 phần tử
            #     param = {key: value[0] if len(value) == 1 else value for key, value in param_dict.items()}
            # else:
            #     param = {}
            
            return query_string, new_path

        # Xử lý các trường hợp push//: và replace//:
        if path.startswith("push//:") or path.startswith("replace//:"):
            path_parts = path.split(':', 1)
            new_path = path_parts[1] if len(path_parts) > 1 else path
            param = path_parts[0]
            
            # Xử lý query string trong push//: hoặc replace//:
            if '?' in new_path:
                path_and_params = new_path.split('?', 1)
                new_path = path_and_params[0]
                query_string = path_and_params[1] if len(path_and_params) > 1 else ""
                if query_string:
                    param_dict = parse_qs(query_string)
                    param = {key: value[0] if len(value) == 1 else value for key, value in param_dict.items()}
            
            return param, new_path

        # Xử lý trường hợp :param trong path
        segments = path.split('/')
        new_segments = []
        
        for seg in segments:
            if ':' in seg:
                param = seg.replace(":", "")
            else:
                new_segments.append(seg)
        
        # Ghép lại các segment thành đường dẫn mới
        new_path = "/".join(new_segments)
        # Đảm bảo đường dẫn bắt đầu bằng '/' nếu đầu vào có
        if path.startswith("/") and not new_path.startswith("/"):
            new_path = "/" + new_path

        return param, new_path

    def get_route(self, route:str="//dashboard///user///profile///", default=None):
        param = None
        if route.find(":") != -1:
            param, route = self.extract_param_and_clean_path(route)
        paths = self.paire_route(route)
        main_path = paths[0]
        current:dict = self.get_dict_route(main_path)
        layout = None
        page = None
        leng = len(paths)
        for i in range(leng):
            path = paths[i]
            _path = current.get("path")
            _type = current.get("type")
            element = current.get("element")
            children = current.get("children")
            index = current.get("index")
            
            if _type == "layout":
                layout = element
            
            if i == leng-1:
                if children:
                    index_true = self.get_index_true(children)
                    # print("index_true", index_true)
                    page = index_true.get("element")
                    return {"layout":layout, "page":page, "param": param}
                page = current.get("element")
                if page == layout:
                    page = None
                return {"layout":layout, "page":page, "param": param}
            else:
                if children:
                    next_path = paths[i+1]
                    current = self.get_current_route(children,next_path)
                    continue
                return {"layout":layout, "page":page, "param": param}
            
# route = RouterParse(list_router=list_rourte)
# # kq = route.get_route("//dashboard---///a--pp//gfgd///")
# kq = route.get_route("dashboard/app")
# kq = route.get_route("dashboard/user")
# print(kq)

