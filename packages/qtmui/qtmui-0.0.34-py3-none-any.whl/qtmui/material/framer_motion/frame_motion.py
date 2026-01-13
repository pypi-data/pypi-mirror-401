# qtmui/material/box/box.py
import asyncio
from functools import lru_cache
import uuid

from typing import Optional, Union, Callable, Dict, List

from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout
from PySide6.QtCore import QTimer, QPoint

from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.utils.data import deep_merge

from qtmui.material.styles import useTheme
from qtmui.hooks import useEffect, State
from qtmui.utils.calc import timer

from qtmui.material.widget_base import PyWidgetBase
from qtmui.material.widget_base.anim_manager import AnimManager
from qtmui.material.widget_base.shadow_effect import ShadownEffect

from qtmui.errors import PyMuiValidationError
from qtmui.material.utils.validate_params import _validate_param
from qtmui.configs import LOAD_WIDGET_ASYNC


class FrameMotion(QFrame, PyWidgetBase, AnimManager):

    def __init__(
        self,
        children: Optional[Union[State, List, str]] = None,
        **kwargs
    ):
        super().__init__()
        self.setObjectName(str(id(self)))
        
        self.destroyed.connect(lambda obj: self._onDestroy())
        
        AnimManager.__init__(self, **kwargs)
        ShadownEffect.__init__(self)
        
        self.theme = useTheme()

        self._set_children(children)

        self._init_ui()

    
    # @_validate_param(file_path=FILE_PATH, param_name="children", supported_signatures=Union[State, list, str, type(None)])
    def _set_children(self, value):
        """Assign value to children and validate."""
        self._children = value  # Chỉ gán, không cập nhật giao diện

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    def _init_ui(self):
        self.setLayout(QVBoxLayout())  # Gán layout ngay lập tức
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self._update_children()

    def _update_children(self):
        """Update layout children."""
        children_value = self._get_children()
        if children_value:
            for widget in children_value:
                if isinstance(widget, QWidget):
                    # if LOAD_WIDGET_ASYNC:
                    #     self._do_task_async(lambda widget=widget: self.layout().addWidget(widget))
                    # else:
                    #     self.layout().addWidget(widget)
                    self.layout().addWidget(widget)

    def _onDestroy(self, obj=None):
        # Cancel task nếu đang chạy
        # if hasattr(self, "_setupStyleSheet") and self._setupStyleSheet and not self._setupStyleSheet.done():
        #     self._setupStyleSheet.cancel()
        if hasattr(self, "_schedule_children_animation_task") and self._schedule_children_animation_task and not self._schedule_children_animation_task.done():
            self._schedule_children_animation_task.cancel()
        if hasattr(self, "_schedule__animCtlPlayTask") and self._schedule__animCtlPlayTask and not self._schedule__animCtlPlayTask.done():
            self._schedule__animCtlPlayTask.cancel()
        try:
            if hasattr(self, "animCtl"):
                self.animCtl.anim_group.stop()
        except Exception as e:
            print("Err: (PySide6.QtCore.QParallelAnimationGroup) already deleted")

    # kiểu này thì các animation của AnimEffect không có
    # QPropertyAnimation::updateState (opacity): Changing state of an animation without target
    # QPropertyAnimation::updateState (scaleX): Changing state of an animation without target
    # QPropertyAnimation::updateState (scaleY): Changing state of an animation without target
    # def showEvent(self, event):
    #     AnimManager.showEvent(self, event)
    #     super().showEvent(event)
        
    # kieu nay thi ok nhưng hiệu ứng chưa phối hợp đẹp
    def showEvent(self, event):
        QTimer.singleShot(0, lambda: AnimManager.showEvent(self, event))
        super().showEvent(event)
        
