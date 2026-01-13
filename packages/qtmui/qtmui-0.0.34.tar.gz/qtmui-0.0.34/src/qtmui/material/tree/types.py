from typing import Optional, List, Dict, Any

# Định nghĩa NavConfigProps như một lớp
class NavConfigProps:
    def __init__(self,
                 hiddenLabel: Optional[bool] = None,
                 itemGap: Optional[int] = None,
                 iconSize: Optional[int] = None,
                 itemRadius: Optional[int] = None,
                 itemPadding: Optional[str] = None,
                 currentRole: Optional[str] = None,
                 itemSubHeight: Optional[int] = None,
                 itemRootHeight: Optional[int] = None):
        self.hiddenLabel = hiddenLabel
        self.itemGap = itemGap
        self.iconSize = iconSize
        self.itemRadius = itemRadius
        self.itemPadding = itemPadding
        self.currentRole = currentRole
        self.itemSubHeight = itemSubHeight
        self.itemRootHeight = itemRootHeight

# Định nghĩa NavListProps như một lớp
class NavListProps:
    def __init__(self,
                 title: str,
                 path: str,
                 icon: Optional[Any] = None,
                 info: Optional[Any] = None,
                 caption: Optional[str] = None,
                 disabled: Optional[bool] = None,
                 roles: Optional[List[str]] = None,
                 children: Optional[Any] = None):
        self.title = title
        self.path = path
        self.icon = icon
        self.info = info
        self.caption = caption
        self.disabled = disabled
        self.roles = roles
        self.children = children

# Định nghĩa NavItemProps như một lớp kế thừa từ NavListProps
class NavItemProps(NavListProps):
    def __init__(self,
                 item: NavListProps,
                 depth: int,
                 active: bool,
                 open: Optional[bool] = None,
                 externalLink: Optional[bool] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.item = item
        self.depth = depth
        self.open = open
        self.active = active
        self.externalLink = externalLink

# Định nghĩa NavSectionProps như một lớp kế thừa từ StackProps
class NavSectionProps:
    def __init__(self,
                 data: List[Dict[str, Any]],
                 config: Optional[NavConfigProps] = None,
                 **kwargs):
        self.data = data
        self.config = config
        for key, value in kwargs.items():
            setattr(self, key, value)

# # Ví dụ sử dụng các lớp
# nav_config = NavConfigProps(hiddenLabel=True, itemGap=10)
# nav_list = NavListProps(title="Home", path="/home")
# nav_item = NavItemProps(item=nav_list, depth=1, active=True)
# nav_section = NavSectionProps(data=[{"subheader": "Main", "items": [nav_list]}], config=nav_config)

# print(vars(nav_config))
# print(vars(nav_list))
# print(vars(nav_item))
# print(vars(nav_section))
