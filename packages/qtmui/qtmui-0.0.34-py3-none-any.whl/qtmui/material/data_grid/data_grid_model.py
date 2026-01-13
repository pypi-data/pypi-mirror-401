from typing import Callable
from PySide6.QtCore import QAbstractTableModel, Qt, Signal, QModelIndex
from PySide6.QtGui import QColor, QFont
# from asyncqt import QtCore

from qtmui.material.styles import useTheme
from qtmui.i18n.use_translation import translate, i18n

class DataGridModel(QAbstractTableModel):
  # https://stackoverflow.com/questions/64287713/how-can-you-set-header-labels-for-qtableview-columns
  set_data = Signal(object,object)

  def headerData(self, section: int, orientation: Qt.Orientation, role: int):
    if orientation == Qt.Horizontal and role == Qt.DisplayRole:
      # return f"Column {section + 1}"
      return self._headerNames[section]
    if orientation == Qt.Vertical and role == Qt.DisplayRole:
      return f"{section + 1}"
    if role == Qt.ForegroundRole:
      return QColor(self.theme.palette.text.secondary)
    if role == Qt.FontRole:
        # Thiết lập kiểu font, kích thước và độ đậm cho header
        font = QFont()
        font.setFamily("Arial")  # Thay "Arial" bằng tên font bạn muốn
        font.setPointSize(10)  # Thay đổi kích thước font theo ý muốn
        font.setBold(True)  # Để đậm font, nếu không cần thì có thể bỏ
        return font

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
    # self.set_data.connect(self._parent.setIndexWidget,Qt.ConnectionType.QueuedConnection)
    self.set_data.connect(self._parent.setIndexWidget)

    self.theme = useTheme()
    self.theme.state.valueChanged.connect(self.__set_stylesheet)
    self.__set_stylesheet()

    i18n.langChanged.connect(self.retranslateUi)
    self.retranslateUi()

  def retranslateUi(self):
    translated_header = []
    for headerName in self._headerNames:
      if isinstance(headerName, Callable):
        translated_header.append(translate(headerName))
      else:
        translated_header.append(headerName)
    self._headerNames = translated_header


  def restranUi(self):
    pass
    # QCoreApplication.translate("MainWindow", u"Form", None)

  def __set_stylesheet(self):
    self.theme = useTheme()


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
          # value = str(self._rows[index.row()][index.column()])
          value = ''
        except IndexError:
          value = ""

      if role == Qt.TextAlignmentRole:
        if self._columns[index.column()].get("align") == "right":
          return int(Qt.AlignRight | Qt.AlignVCenter)
        elif self._columns[index.column()].get("align") == "center":
          return int(Qt.AlignCenter | Qt.AlignVCenter)
        else: # left
          # print('lefffffffffff___________')
          return int(Qt.AlignLeft | Qt.AlignVCenter)


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
