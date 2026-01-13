from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QTableView, QProxyStyle, QStyleOption, QHeaderView, QAbstractItemView

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




