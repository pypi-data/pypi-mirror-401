
from typing import Optional, Callable




# from ...utils.data import deep_merge

class StyledOptions:
    shouldForwardProp: Optional[str] 
    label: Optional[str] 
    name: Optional[str] 
    slot: Optional[str] 
    overridesResolver: Optional[Callable] 
    skipVariantsResolver: Optional[bool] 
    skipSx: Optional[bool] 

def styled(component, options: dict={}, styleFn: Callable=None):
    """
    Tạo ra một styled component dựa trên component gốc và hàm styleFn.
    
    styleFn có thể là một hàm nhận vào (props, theme) và trả về một dictionary chứa style,
    hoặc đơn giản là một dictionary.
    """

    shouldForwardProp = options.get("shouldForwardProp") 
    label = options.get("label") 
    name = options.get("name") 
    slot = options.get("slot") 
    overridesResolver = options.get("overridesResolver") 
    skipVariantsResolver = options.get("skipVariantsResolver") 
    skipSx = options.get("skipSx") 


    class StyledComponent(component):
        def __init__(self, *args, **kwargs):
            # Lưu props nếu cần
            self.props = kwargs.copy()
            self._setProps(kwargs)
            
            # if shouldForwardProp:
            #     for key, value in self.props.items():
            #         if shouldForwardProp(key):
            #             self.setProperty(key, value)
            #             self.style().unpolish(self)
            #             self.style().polish(self)
            #             self.update()
            
            self._setStyledDict(styleFn=styleFn)
            super().__init__(*args, **kwargs)

            if styleFn:
                if shouldForwardProp:
                    for key, value in self.props.items():
                        if shouldForwardProp(key):
                            self.setProperty(key, value)
                            self.style().unpolish(self)
                            self.style().polish(self)
                            self.update()

                # self.setProperty("styled")
                # self.setProperty("overidde")
                # self.setProperty("sx")

                # Chuyển đổi style thành chuỗi QSS và áp dụng
                # if hasattr(self, "component_styles"):
                #     component_styles = deep_merge(self.component_styles, styleFn())
                #     self._set_stylesheet(component_styles)

        @classmethod
        def _setProps(cls, props={}):
            cls.props = props
            
        @classmethod
        def _setStyledDict(cls, styleFn: Callable=None):
            if isinstance(styleFn, Callable):
                cls.styledDict = styleFn()
            else:
                cls.styledDict = {}

    return StyledComponent

