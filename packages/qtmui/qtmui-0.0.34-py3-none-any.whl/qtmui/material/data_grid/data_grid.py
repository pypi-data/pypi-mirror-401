import asyncio
import threading
from typing import Callable

from PySide6.QtCore import Qt, QModelIndex, Signal, QTimer
from PySide6.QtWidgets import QHeaderView, QAbstractItemView, QTableView, QProxyStyle, QStyleOption

from .frozen_column import FrozenColumn

from .data_grid_model import DataGridModel
from ..widget_base import PyWidgetBase

from qtmui.material.styles import useTheme

class DataGrid(QTableView, PyWidgetBase):

  setIndexWidgetSignal = Signal(QModelIndex)

  class DropmarkerStyle(QProxyStyle):
    def drawPrimitive(self, element, option, painter, widget=None):
      """Draw a line across the entire row rather than just the column we're hovering over.
      This may not always work depending on global style - for instance I think it won't
      work on OSX."""
      if str(
        element) == "PrimitiveElement.PE_IndicatorItemViewItemDrop" and not option.rect.isNull():  # element == self.PE_IndicatorItemViewItemDrop and
        option_new = QStyleOption(option)
        option_new.rect.setLeft(0)
        if widget:
          option_new.rect.setRight(widget.width())
        option = option_new
      super().drawPrimitive(element, option, painter, widget)

  def __init__(
      self,

      columns,
      rows,
      checkboxSelection=False,
      disableRowSelectionOnClick=False,

      context=None,
      id: str = None,
      isDense: bool = None,
      isManyRows: bool = None,
      fullWidth: bool = True,
      tableHead: list = None,
      singleSelection: bool = False,
      stretchLastSection: bool = False,
      model=None,
      selectionChanged: Callable = None,
      itemDelegates=None,
      backgroundColor: str = "#ffffff",
      isFrozenLastColumn=None
      ):
    super(DataGrid, self).__init__()
    if id is not None:
      self.setObjectName(id)


    self._columns = columns
    self._rows = rows
    self._checkboxSelection = checkboxSelection
    self._disableRowSelectionOnClick = disableRowSelectionOnClick
    
    self._background_color = "transparent"
    self._isDense = isDense
    self._isManyRows = isManyRows
    self._fullWidth = fullWidth
    self._tableHead = tableHead
    # self._model = model
    self._stretchLastSection = stretchLastSection
    self._isFrozenLastColumn = isFrozenLastColumn
    self._itemDelegates = itemDelegates
    self._selectionChanged = selectionChanged
    self._singleSelection = singleSelection

    self._frozenColumn = None

    self._is_filter_mode = False
    self._column_count = len(self._columns)

    self.last_drop_row = None
    self.lastCol = len(self._columns) - 1

    # if self._selectionChanged is not None:
    #   # self.pressed.connect(self._selectionChanged)
    #   self.selectionModel().selectionChanged.connect(self._selectionChanged)

    self._model = DataGridModel(self, self._columns, self._rows)


    self.setAttribute(Qt.WA_Hover, True)

    self.setupUi()

    self.setIndexWidgetSignal.connect(self._set_index_widget)


  def _thread_set_index_widget(self):
    for i in range(len(self._columns)):
      for j in range(len(self._rows)):
        self.setIndexWidgetSignal.emit(self._model.index(j, i))

  def _set_index_widget(self, index):
    renderCell = self._columns[index.column()].get("renderCell")
    if renderCell:
      options = self._rows[index.row()]
      cell = renderCell(options)
      self.setIndexWidget(index, cell)


  def setupUi(self):
    self.setDragEnabled(True)
    self.setAcceptDrops(True)
    self.setDragDropOverwriteMode(False)
    # self.setStyle(self.DropmarkerStyle())

    if self._isFrozenLastColumn == True:
      self._frozenColumn = FrozenColumn(parent=self, lastCol=self.lastCol)

    self.update_model(self._model)

    self._horizontalHeader = self.horizontalHeader()
    self._horizontalHeader.setMinimumWidth(200)

    self.horizontalHeader().sectionResized.connect(self.updateSectionWidth)
    self.verticalHeader().sectionResized.connect(self.updateSectionHeight)

    if self._stretchLastSection == True:
      self.horizontalHeader().setStretchLastSection(True)

    if self._singleSelection:
      self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
    else:
      self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
      self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

    if self._isFrozenLastColumn == True:
      self.viewport().stackUnder(self._frozenColumn)
    self.viewport().setContentsMargins(0, 0, 0, 0)

    self.header = self.horizontalHeader()
    self.header.setDefaultAlignment(Qt.AlignLeft)
    
    self.verticalHeader().hide()

    self.setViewportMargins(0, 0, 0, 0)
    self.setSortingEnabled(True)
    self.setDragEnabled(True)

    self.setWordWrap(False)

    self.verticalHeader().setDefaultSectionSize(40)

    self.theme = useTheme()
    self.theme.state.valueChanged.connect(self.slot_set_stylesheet)
    self.destroyed.connect(self._on_destroyed)
    self.slot_set_stylesheet()

  def slot_set_stylesheet(self, value=None):
      self._set_stylesheet()

  def _set_stylesheet(self, component_styled=None):
    self.theme = useTheme()

    ownerState = {}

    if not component_styled:
        component_styled = self.theme.components

    self.setStyleSheet(f"""
        QWidget {{
                background-color: transparent;
        }}
        QTableView {{
            background-color: transparent;
            padding: 0px;
            border: none;
            gridline-color: transparent;
            color: {self.theme.palette.text.secondary};
        }}

        QTableView::item {{
            padding-left: 0px;
            padding-right: 5px;
        }}

        QTableView::item:selected {{
            background-color: {self.theme.palette.action.selected};
            color: {self.theme.palette.text.secondary};
        }}

        QTableView::section {{
            background-color: transparent;
            max-width: 30px;
            text-align: left;

        }}

        QTableView::horizontalHeader {{
            background-color: red;
            color: {self.theme.palette.text.primary};
            font-size: {self.theme.typography.button.fontSize};
            font-weight: {self.theme.typography.button.fontWeight};
            line-height: {self.theme.typography.button.lineHeight};
        }}

        QTableView::section:horizontal {{
            background-color: transparent;
            padding: 0px;
            border: 1px solid red !important;
            border-bottom: 1px solid red !important;
        }}


        QTableView::section:vertical {{
            border: 1px solid red;
        }}

        QTableView .QScrollBar:horizontal {{
            border: none;
            background: transparent;
            min-height: 8px;
            border-radius: 0px;
            max-width: 79em;
        }}

        QTableView .QHeaderView::section {{
            background-color: transparent!important;
        }}

      """)

  def update_model(self, model=None):
    # print('update_model______________', self._model._data)
    if model == None:
      model = self._model

    self.setModel(model)
    # self.update(model)

    # self.setItemDelegateForColumn(5, ButtonDelegate(self))

    # if isinstance(self._itemDelegates, list):
    #   for item in self._itemDelegates:
    #     item.parent = self
    #     self.setItemDelegateForColumn(2, item)

    if self._isFrozenLastColumn == True:
      self._frozenColumn.setModel(model)
      self._frozenColumn.setupUi()
      self.updateFrozenTableGeometry()
      self._frozenColumn.setFocusPolicy(Qt.NoFocus)
      self._frozenColumn.configTable(self.selectionModel())
      self._itemDelegates[-1].parent = self._frozenColumn
      self._frozenColumn.setItemDelegateForColumn(self.lastCol, self._itemDelegates[-1])
      if not self.isVisible():
        self.show()

    if self._selectionChanged is not None:
      # self.pressed.connect(self._selectionChanged)
      self.selectionModel().selectionChanged.connect(self._selectionChanged)

    self.configUiTableView()

  def configUiTableView(self):
    self.verticalHeader().hide()

    self.setViewportMargins(0, 0, 0, 0)
    
    self._horizontalHeader = self.horizontalHeader()
    self.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    # for index, item in enumerate(self._tableHead):
    #   if item.get('resizeMode') == "ResizeToContents":
    #     self._horizontalHeader.setSectionResizeMode(index, QHeaderView.ResizeToContents)
    #   if item.get('resizeMode') == "Fixed":
    #     self._horizontalHeader.setSectionResizeMode(index, QHeaderView.Fixed)
    #     self.setColumnWidth(index, item.get('width'))
    #   if item.get('resizeMode') == "Stretch":
    #     self._horizontalHeader.setSectionResizeMode(index, QHeaderView.Stretch)
    #   if item.get('columnHidden') == True:
    #     self.setColumnHidden(index, True)

    # sorted_dict = {
    #     "align": 'right',
    #     "description": 'This column has a value getter and is not sortable.',
    #     "disableColumnMenu": True,
    #     "editable": True,
    #     "field": 'age',
    #     "flex": 1,
    #     "headerAlign": 'center',
    #     "headerName": 'Age',
    #     "renderCell": lambda: print('renderCell'),
    #     "sortable": False,
    #     "type": 'number',
    #     "valueGetter": lambda params: f'{params.row.firstName | ""} {params.row.lastName | ""}',
    #     "width": 120,
    # }

    for index, item in enumerate(self._columns):
      if item.get('align'):
        pass
      if item.get('description'):
        pass
      if item.get('disableColumnMenu'):
        pass
      if item.get('editable'):
        pass
      if item.get('field'):
        pass
      if item.get('flex'):
        pass
      if item.get('headerAlign'):
        pass
      if item.get('headerName'):
        pass
      if item.get('renderCell'):
        # delegate = item.get('renderCell')()
        # delegate = item.get('renderCell')
        # delegate.parent = self
        # print('delegate______________', index, delegate)
        # self.setItemDelegateForColumn(index, delegate)
        pass
      if item.get('sortable'):
        pass
      if item.get('type'):
        pass
      if item.get('valueGetter'):
        pass
      if item.get('width'):
        pass


    



  def updateSectionWidth(self, logicalIndex, oldSize, newSize):
    if self._isFrozenLastColumn is not None and logicalIndex == self.lastCol:
      self._frozenColumn.setColumnWidth(self.lastCol, newSize)
    self.updateFrozenTableGeometry()

  def updateSectionHeight(self, logicalIndex, oldSize, newSize):
    if  self._frozenColumn is not None:
      self._frozenColumn.setRowHeight(logicalIndex, newSize)

  def resizeEvent(self, event):
    super(DataGrid, self).resizeEvent(event)
    self.updateFrozenTableGeometry()

  def moveCursor(self, cursorAction, modifiers):
    current = super(DataGrid, self).moveCursor(cursorAction, modifiers)
    if (cursorAction == QAbstractItemView.MoveLeft and current.column() < self.lastCol and
      self.visualRect(current).topLeft().x() < (self._frozenColumn.columnWidth(self.lastCol))):
      newValue = (self.horizontalScrollBar().value() +
                  self.visualRect(current).topLeft().x() - self._frozenColumn.columnWidth(self.lastCol))
      self.horizontalScrollBar().setValue(newValue)
    return current

  def scrollTo(self, index, hint):
    if index.column() < self.lastCol:
      super(DataGrid, self).scrollTo(index, hint)

  def updateFrozenTableGeometry(self):
    x_position = self.verticalHeader().width() + self.frameWidth()
    for col in range(0, self.lastCol):
      x_position += self.columnWidth(col)
    x_viewPort = self.verticalHeader().width() + self.viewport().width() - self.columnWidth(
      self.lastCol) + self.frameWidth()
    if self._isFrozenLastColumn is not None:
      self._frozenColumn.setGeometry(x_position if x_position < x_viewPort else x_viewPort,
                                      self.frameWidth(), self.columnWidth(self.lastCol),
                                      self.viewport().height() + self.horizontalHeader().height())


  def cellButtonClicked(self, data):
    print('data_________', data)
    arr_info = data.split('_')
    btn_name = arr_info[0]
    index_row = int(arr_info[1])
    id_profile = self.model().index(index_row, 1).data()
    profile_name = self._main_window.tblProfile._model._data[index_row][3]
    self.profile_id_selected = id_profile


  def dropEvent(self, event):
    sender = event.source()
    super().dropEvent(event)
    dropRow = self.last_drop_row
    destination = self.objectName()
    to_index = self.indexAt(event.pos()).row()

    selectedRows = sender.getselectedRowsFast()

    arr_id_profile = []

    model = sender.model()
    for srow in selectedRows:
      id = model.index(srow, 1).data()
      arr_id_profile.append(int(id))

    event.accept()


  def getselectedRowsFast(self):
    selectedRows = []
    # for item in self.selectedItems():
    for item in self.selectedIndexes():
      if item.row() not in selectedRows:
        selectedRows.append(item.row())
    selectedRows.sort()
    return selectedRows



