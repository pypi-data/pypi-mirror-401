import asyncio
from functools import lru_cache
from typing import Optional, Union, Callable, Any, List, Dict
import uuid

from qtmui.hooks import State
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QSizePolicy, QHBoxLayout
from PySide6.QtCore import Qt, QTimer

from ..widget_base import PyWidgetBase
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ..utils.validate_params import _validate_param

class TableHead:

    def __init__(
        self,
        children: Optional[Union[State, Any, List[Any]]] = None,
        order: Union[State, str] = None,
        checked: Union[State, str] = None,
        orderBy: Union[State, str] = None,
        headLabel: Union[State, List[Any]] = None,
        rowCount: Union[State, int] = None,
        numSelected: Union[State, int] = 0,
        onSort: Union[State, Callable] = None,
        onSelectAllRows: Union[State, Callable] = None,
        tableSelectedAction: Union[State, QWidget] = None,
    ):

        self._children = children
        self._order = order
        self._orderBy = orderBy
        self._headLabel = headLabel
        self._rowCount = rowCount
        self._numSelected = numSelected
        self._onSort = onSort
        self._onSelectAllRows = onSelectAllRows
        self._tableSelectedAction = tableSelectedAction
        
        # self._numSelected.valueChanged.connect(lambda: print('_numSelected', self._numSelected.value))

