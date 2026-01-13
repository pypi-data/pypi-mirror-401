import sys
import threading
from typing import Callable

from PySide6.QtCore import Qt, QModelIndex, Signal, QAbstractTableModel
from PySide6.QtWidgets import QPushButton, QWidget, QMainWindow, QHeaderView, QAbstractItemView, QTableView, QProxyStyle, QStyleOption,  QTableView, QProxyStyle, QStyleOption, QHeaderView, QAbstractItemView, QApplication
from PySide6.QtGui import QColor


class FrozenColumn(QTableView):
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
              parent=None, 
              context=None,
              lastCol: int = None
              ):
    super(FrozenColumn, self).__init__()
    self.setParent(parent)
    self.dist_btn_data_new = {}
    self.last_drop_row = None
    self.lastCol = lastCol

    print("self.lastCol_______________", self.lastCol)


  def setupUi(self):
    self.verticalScrollBar().valueChanged.connect(
      self.parent().verticalScrollBar().setValue)
    self.parent().verticalScrollBar().valueChanged.connect(
      self.verticalScrollBar().setValue)
    self.setFocusPolicy(Qt.NoFocus)
    self.verticalHeader().hide()
    self.setMinimumWidth(110)
    self.horizontalHeader().setMinimumSectionSize(110)
    self.setDragEnabled(True)
    self.setAcceptDrops(True)
    self.setDragDropOverwriteMode(False)
    # self.setStyle(self.DropmarkerStyle())
    
    for col in range(0, self.lastCol):
      self.setColumnHidden(col, True)

    self.horizontalHeader().setSectionResizeMode(self.lastCol, QHeaderView.ResizeMode.Fixed)
    self.setColumnWidth(self.lastCol, 300)  # Proxy

  def configTable(self, selectionModel):
    self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
    self.setSelectionModel(selectionModel)

  def data(self, index, role):
    if role == Qt.BackgroundRole:
      return QColor(18, 219, 187)
      # return QBrush(Qt.yellow)

  def cellButtonClicked(self, data):
    print('data_________', data)
    arr_info = data.split('_')
    btn_name = arr_info[0]
    index_row = int(arr_info[1])
    id_profile = self.model().index(index_row, 1).data()
    self.profile_id_selected = id_profile


  def getselectedRowsFast(self):
    selectedRows = []
    # for item in self.selectedItems():
    for item in self.selectedIndexes():
      if item.row() not in selectedRows:
        selectedRows.append(item.row())
    selectedRows.sort()
    return selectedRows





class DataGridModel(QAbstractTableModel):
  # https://stackoverflow.com/questions/64287713/how-can-you-set-header-labels-for-qtableview-columns
  set_data = Signal(object,object)
  def headerData(self, section: int, orientation: Qt.Orientation, role: int):
    if orientation == Qt.Horizontal and role == Qt.DisplayRole:
      # return f"Column {section + 1}"
      return self._headerNames[section]
    if orientation == Qt.Vertical and role == Qt.DisplayRole:
      return f"{section + 1}"

  def __init__(self, 
               parent=None, 
               columns=None,
               rows=None,
               ):
    # self.setRowCount(0)
    self._headerNames = [item.get('headerName') if item.get('headerName') else ""  for item in columns]
    
    super(DataGridModel, self).__init__(parent)

    self._parent = parent
    self._columns = columns
    self._rows = rows
    self.colors = dict()
    self.set_data.connect(self._parent.setIndexWidget)

  def restranUi(self):
    pass

  def rowCount(self, n=None):
    return len(self._rows)

  def columnCount(self, n=None):
    return len(self._columns)

  def flags(self, index: QModelIndex) -> Qt.ItemFlags:
    return Qt.ItemIsDropEnabled | Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled

  def supportedDropActions(self) -> bool:
    return Qt.MoveAction | Qt.CopyAction

  def _thread_set_index_model(self, index, widget):
    self.set_data.emit(index, widget)


  def data(self, index, role=Qt.ForegroundRole):
    if index.isValid():
      if role == Qt.ItemDataRole.DisplayRole or role == Qt.EditRole:
        try:
          renderCell = self._columns[index.column()].get("renderCell")
          if renderCell:
            # options = self._rows[index.row()]
            # cell = renderCell(options)
            # if not self.parent().indexWidget(index):
            #   pass
            value = ""
          else:
            value = str(self._rows[index.row()][self._columns[index.column()].get("field")])

        except Exception as e:
          print(str(e))
          value = None
        return value or ""

      if role == Qt.BackgroundRole:
        # color = self.colors.get((index.row(), index.column()))
        color = None
        if color is not None:
          return color

      if role == Qt.ForegroundRole:
        try:
          value = ''
        except IndexError:
          value = ""


  def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
    try:
      curentValue = self._rows[index.row()][self._columns[index.column()].get("field")]
    except IndexError:
      curentValue = ' '
    if not index.isValid():
      return False

    if role == Qt.ItemDataRole.EditRole:
      #print(377, 'setData tableView')
      if value == "":
        return False
      if value != curentValue and value != "":
        try:
          self._rows[index.row()][self._columns[index.column()].get("field")]= value
        except:
          return False
      else:
        self._rows[index.row()][self._columns[index.column()].get("field")] = curentValue
      return True

    return False

  # @QtCore.Slot(int, int, QtCore.QVariant)
  def update_item(self, row, col, value):
    ix = self.index(row, col)
    self.setData(ix, value)
    
  def change_color(self, row, column, color):
    ix = self.index(row, column)
    self.colors[(row, column)] = color
    self.dataChanged.emit(ix, ix, (Qt.BackgroundRole,))



class DataGrid(QTableView):

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

    # model = self.model()


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

    self.setStyleSheet(f"""

        QTableView {{
            background-color: transparent;
            padding: 0px;
            border: none;
            gridline-color: transparent;
            color: #6b6b6b;
        }}

        QTableView::item {{
            padding-left: 0px;
            padding-right: 5px;
        }}

        QTableView::item:selected {{
            background-color: rgba(242, 242, 242, 0.8);
            color: #6b6b6b;
        }}

        QTableView::section {{
            background-color: transparent;
            max-width: 30px;
            text-align: left;

        }}

        QTableView::horizontalHeader {{
            background-color: transparent;

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1600, 900)

        columns = [
            {
                "field": 'id',
            },
            {
                "field": 'avatar',
                "headerName": 'Avatar',
                "align": 'center',
                "headerAlign": 'center',
                "width": 64,
                "sortable": False,
                "filterable": False,
                "disableColumnMenu": True,
                "renderCell": lambda params: QPushButton("Avatar"),
            },
            {
                "field": 'name',
                "headerName": 'Name',
                "flex": 1,
                "editable": True,
            },
            {
                "field": 'email',
                "headerName": 'Email',
                "flex": 1,
                "editable": True,
                "renderCell": lambda params: QPushButton("Email")
            },
            {
                "field": 'lastLogin',
                "type": 'dateTime',
                "headerName": 'Last login',
                "align": 'right',
                "headerAlign": 'right',
                "width": 200,
            },
            {
                "field": 'rating',
                "type": 'number',
                "headerName": 'Rating',
                "width": 160,
                "disableColumnMenu": True,
                "renderCell": lambda params: QPushButton("Rating")
            },
            {
                "field": 'status',
                "type": 'singleSelect',
                "headerName": 'Status',
                "valueOptions": ['online', 'alway', 'busy'],
                "align": 'center',
                "headerAlign": 'center',
                "width": 120,
                "renderCell": lambda params: QPushButton("Status")
            },
            {
                "field": 'isAdmin',
                "headerName": 'isAdmin',
                "type": 'boolean',
                "align": 'center',
                "headerAlign": 'center',
                "width": 120,
                "renderCell": lambda params: QPushButton("isAdmin")
            },
            {
                "field": 'performance',
                "type": 'number',
                "headerName": 'Performance',
                "align": 'center',
                "headerAlign": 'center',
                "width": 160,
                "renderCell": lambda params: QPushButton("Performance")
            },
            {
                "field": 'action',
                "headerName": ' ',
                "align": 'right',
                "width": 80,
                "sortable": False,
                "filterable": False,
                "disableColumnMenu": True,
                "renderCell": lambda params: QPushButton("Performance")
            },
        ]


        data = [
            {
                'id': f"{index}",
                'status': "status",
                'email': "email",
                'name': "name",
                'age': "age",
                # 'avatar': ":/IconLight/resources/IconLight/Folder.svg",
                'lastLogin': "lastLogin",
                'isAdmin': "isAdmin",
                'lastName': "lastName",
                'rating': "rating",
                'firstName': "firstName",
                'performance': "performance",
            }
            for index in range(400)
        ]

        self.setCentralWidget(
            DataGrid(
                columns=columns,
                rows=data,
                checkboxSelection=True,
                disableRowSelectionOnClick=True
            )
        )

            
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()