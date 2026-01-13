from typing import Optional

class NavConfigProps:
    def __init__(self,
                 hiddenLabel: Optional[bool] = False,
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

def navVerticalConfig(config: Optional[NavConfigProps] = None) -> dict:
    config = config or NavConfigProps()
    return {
        'itemGap': config.itemGap if config.itemGap is not None else 4,
        'iconSize': config.iconSize if config.iconSize is not None else 24,
        'currentRole': config.currentRole,
        'itemRootHeight': config.itemRootHeight if config.itemRootHeight is not None else 44,
        'itemSubHeight': config.itemSubHeight if config.itemSubHeight is not None else 36,
        'itemPadding': config.itemPadding if config.itemPadding is not None else '4px 8px 4px 12px',
        'itemRadius': config.itemRadius if config.itemRadius is not None else 8,
        'hiddenLabel': config.hiddenLabel if config.hiddenLabel is not None else False,
    }

def navMiniConfig(config: Optional[NavConfigProps] = None) -> dict:
    config = config or NavConfigProps()
    return {
        'itemGap': config.itemGap if config.itemGap is not None else 4,
        'iconSize': config.iconSize if config.iconSize is not None else 22,
        'currentRole': config.currentRole,
        'itemRootHeight': config.itemRootHeight if config.itemRootHeight is not None else 56,
        'itemSubHeight': config.itemSubHeight if config.itemSubHeight is not None else 34,
        'itemPadding': config.itemPadding if config.itemPadding is not None else '6px 0 0 0',
        'itemRadius': config.itemRadius if config.itemRadius is not None else 6,
        'hiddenLabel': config.hiddenLabel if config.hiddenLabel is not None else False,
    }

def navHorizontalConfig(config: Optional[NavConfigProps] = None) -> dict:
    config = config or NavConfigProps()
    return {
        'itemGap': config.itemGap if config.itemGap is not None else 6,
        'iconSize': config.iconSize if config.iconSize is not None else 22,
        'currentRole': config.currentRole,
        'itemRootHeight': config.itemRootHeight if config.itemRootHeight is not None else 32,
        'itemSubHeight': config.itemSubHeight if config.itemSubHeight is not None else 34,
        'itemPadding': config.itemPadding if config.itemPadding is not None else '0 6px 0 6px',
        'itemRadius': config.itemRadius if config.itemRadius is not None else 6,
        'hiddenLabel': config.hiddenLabel if config.hiddenLabel is not None else False,
    }

# # Ví dụ sử dụng các hàm
# nav_config = NavConfigProps(itemGap=10, iconSize=30)
# print(navVerticalConfig(nav_config))
# print(navMiniConfig(nav_config))
# print(navHorizontalConfig(nav_config))
