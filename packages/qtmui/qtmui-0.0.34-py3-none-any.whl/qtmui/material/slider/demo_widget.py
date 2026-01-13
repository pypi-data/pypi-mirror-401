from .qtrangeslider import QRangeSlider
from PySide6 import QtCore
from PySide6 import QtWidgets as QtW

QSS = """
                QSlider:horizontal {
                        min-height: 24px;
                }

                QSlider::groove:horizontal {
                        height: 4px;
                        background-color: rgba(0, 0, 0, 100);
                        border-radius: 2px;
                }

                QSlider::sub-page:horizontal {
                        background: #00A76F;
                        height: 4px;
                        border-radius: 2px;
                }

                QSlider::handle:horizontal {
                        border: 1px solid rgb(222, 222, 222);
                        width: 20px;
                        min-height: 24px;
                        margin: -9px 0;
                        border-radius: 11px;
                        background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,
                                stop:0 #00A76F,
                                stop:0.48 #00A76F,
                                stop:0.55 rgb(255, 255, 255),
                                stop:1 rgb(255, 255, 255));
                }

                QSlider::handle:horizontal:hover {
                        background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,
                                stop:0 #00A76F,
                                stop:0.55 #00A76F,
                                stop:0.65 rgb(255, 255, 255),
                                stop:1 rgb(255, 255, 255));
                }

                QSlider::handle:horizontal:pressed {
                        background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,
                                stop:0 #00A76F,
                                stop:0.4 #00A76F,
                                stop:0.5 rgb(255, 255, 255),
                                stop:1 rgb(255, 255, 255));
                }

                QSlider::groove:horizontal:disabled {
                        background-color: rgba(0, 0, 0, 75);
                }

                QSlider::handle:horizontal:disabled {
                        background-color: #808080;
                        border: 5px solid #cccccc;
                }


                QSlider:vertical {
                        min-width: 24px;
                }

                QSlider::groove:vertical {
                        width: 4px;
                        background-color: rgba(0, 0, 0, 100);
                        border-radius: 2px;
                }

                QSlider::add-page:vertical {
                        background: #00A76F;
                        width: 4px;
                        border-radius: 2px;
                }

                QSlider::handle:vertical {
                        border: 1px solid rgb(222, 222, 222);
                        height: 20px;
                        min-width: 24px;
                        margin: 0 -9px;
                        border-radius: 11px;
                        background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,
                                stop:0 #00A76F,
                                stop:0.48 #00A76F,
                                stop:0.55 rgb(255, 255, 255),
                                stop:1 rgb(255, 255, 255));
                }

                QSlider::handle:vertical:hover {
                        background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,
                                stop:0 #00A76F,
                                stop:0.55 #00A76F,
                                stop:0.65 rgb(255, 255, 255),
                                stop:1 rgb(255, 255, 255));
                }

                QSlider::handle:vertical:pressed {
                        background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,
                                stop:0 #00A76F,
                                stop:0.4 #00A76F,
                                stop:0.5 rgb(255, 255, 255),
                                stop:1 rgb(255, 255, 255));
                }

                QSlider::groove:vertical:disabled {
                        background-color: rgba(0, 0, 0, 75);
                }

                QSlider::handle:vertical:disabled {
                        background-color: #808080;
                        border: 5px solid #cccccc;
                }
        """

SYSTEM_QSS = """
                QSlider::handle:horizontal {
                        background-color: #00A76F;
                }
                QSlider::handle:vertical {
                        background-color: #00A76F;
                }

        """


class DemoWidget(QtW.QWidget):
    def __init__(self) -> None:
        super().__init__()

        reg_hslider = QtW.QSlider(QtCore.Qt.Horizontal)
        reg_hslider.setValue(50)
        range_hslider = QRangeSlider(QtCore.Qt.Horizontal)
        range_hslider.setValue((20, 80))
        multi_range_hslider = QRangeSlider(QtCore.Qt.Horizontal)
        multi_range_hslider.setValue((11, 33, 66, 88))
        multi_range_hslider.setTickPosition(QtW.QSlider.TicksAbove)
        reg_hslider.setStyleSheet(SYSTEM_QSS)
        range_hslider.setStyleSheet(SYSTEM_QSS)
        multi_range_hslider.setStyleSheet(SYSTEM_QSS)

        styled_reg_hslider = QtW.QSlider(QtCore.Qt.Horizontal)
        styled_reg_hslider.setValue(50)
        styled_reg_hslider.setStyleSheet(QSS)
        styled_range_hslider = QRangeSlider(QtCore.Qt.Horizontal)
        styled_range_hslider.setValue((20, 80))
        styled_range_hslider.setStyleSheet(QSS)

        reg_vslider = QtW.QSlider(QtCore.Qt.Vertical)
        reg_vslider.setValue(50)
        range_vslider = QRangeSlider(QtCore.Qt.Vertical)
        range_vslider.setValue((22, 77))
        reg_vslider.setStyleSheet(SYSTEM_QSS)
        range_vslider.setStyleSheet(SYSTEM_QSS)

        tick_vslider = QtW.QSlider(QtCore.Qt.Vertical)
        tick_vslider.setValue(55)
        tick_vslider.setTickPosition(QtW.QSlider.TicksRight)
        tick_vslider.setStyleSheet(SYSTEM_QSS)

        range_tick_vslider = QRangeSlider(QtCore.Qt.Vertical)
        range_tick_vslider.setValue((22, 77))
        range_tick_vslider.setTickPosition(QtW.QSlider.TicksLeft)
        range_tick_vslider.setStyleSheet(SYSTEM_QSS)

        szp = QtW.QSizePolicy.Maximum
        left = QtW.QWidget()
        left.setLayout(QtW.QVBoxLayout())
        left.setContentsMargins(2, 2, 2, 2)
        label1 = QtW.QLabel("Regular QSlider Unstyled")
        label2 = QtW.QLabel("QRangeSliders Unstyled")
        label3 = QtW.QLabel("Styled Sliders (using same stylesheet)")
        label1.setSizePolicy(szp, szp)
        label2.setSizePolicy(szp, szp)
        label3.setSizePolicy(szp, szp)
        left.layout().addWidget(label1)
        left.layout().addWidget(reg_hslider)
        left.layout().addWidget(label2)
        left.layout().addWidget(range_hslider)
        left.layout().addWidget(multi_range_hslider)
        left.layout().addWidget(label3)
        # left.layout().addWidget(styled_reg_hslider)
        # left.layout().addWidget(styled_range_hslider)

        right = QtW.QWidget()
        right.setLayout(QtW.QHBoxLayout())
        right.setContentsMargins(15, 5, 5, 0)
        right.layout().setSpacing(30)
        right.layout().addWidget(reg_vslider)
        right.layout().addWidget(range_vslider)
        right.layout().addWidget(tick_vslider)
        right.layout().addWidget(range_tick_vslider)

        self.setLayout(QtW.QHBoxLayout())
        self.layout().addWidget(left)
        self.layout().addWidget(right)
        self.setGeometry(600, 300, 580, 300)
        self.activateWindow()
        # self.show()

