import uuid
from PySide6.QtWidgets import QHBoxLayout, QFrame

styles = """
        #{} {{
            border: {};
            margin: {};
            font-weight: {};
            line-height: {};
            font-size: {};
            font-family: {};
            padding: {};
            border-radius: {};
            color:  {};
            background-color: {};
        }}
        #{}::hover {{
            background-color: {};
        }}

"""


class ToolBar(QFrame):
# class Chip(QWidget):
    """
    props: AdditionalProps & {
        /**
        * The Toolbar children, usually a mixture of `IconButton`, `Button` and `Typography`.
        * The Toolbar is a flex container, allowing flex item properties to be used to lay out the children.
        */
        children?: React.ReactNode;
        /**
        * Override or extend the styles applied to the component.
        */
        classes?: Partial<ToolbarClasses>;
        /**
        * If `true`, disables gutter padding.
        * @default false
        */
        disableGutters?: boolean;
        /**
        * The variant to use.
        * @default 'regular'
        */
        variant?: OverridableStringUnion<'regular' | 'dense', ToolbarPropsVariantOverrides>;
        /**
        * The system prop that allows defining system overrides as well as additional CSS styles.
        */
        sx?: SxProps<Theme>;
    };
    defaultComponent: DefaultComponent;
    """
    def __init__(self,
                variant: str = None,
                disableGutters: bool = None,
                sx: dict = None,
                children: list = None,
                height: int = 50,
                 *args, 
                 **kwargs
                 ):
        super(ToolBar, self).__init__()
        self.setObjectName(str(uuid.uuid4()))
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.setFixedHeight(height)
        # self.setStyleSheet('''#{}  {{ {} }}'''.format(self.objectName(), "background-color: pink;"))

        self._variant = variant
        self._disableGutters = disableGutters
        self._sx = sx
        self._children = children

         # Thêm các children (nếu có)
        if self._children:
            if not isinstance(self._children, list):
                raise TypeError("children must be type (list)")
            for child in self._children:
                self.layout().addWidget(child)