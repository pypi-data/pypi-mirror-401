import uuid
from typing import Optional, Callable, Union, List, Dict
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QSizePolicy, QCalendarWidget
from PySide6.QtCore import Signal, QSize

from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

from qtmui.i18n.use_translation import i18n

class DateTimePicker(QCalendarWidget):

    def __init__(
                self,
                anchorEl: QWidget=None
                ):
        super().__init__()
        self.setObjectName(u"calendarview")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(0, 300))
        self.setMaximumSize(QSize(320, 300))
        self.setStyleSheet(u"")
        self.setGridVisible(True)
        self.setSelectionMode(QCalendarWidget.SingleSelection)
        self.setHorizontalHeaderFormat(QCalendarWidget.NoHorizontalHeader)
        self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.setNavigationBarVisible(True)
        self.setDateEditEnabled(True)

        self._border_style = ""

        self.__init_ui()

        theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()

        # i18n.langChanged.connect(self.reTranslation)

    def reTranslation(self):
        pass

    def __init_ui(self):
        pass

    def _set_stylesheet(self):
        theme = useTheme()

        self.setStyleSheet(
            f"""
                    QWidget {{
                        background-color: red; 
                        color:{theme.palette.text.primary};
                        border: solid;
                        border-width: 0px;
                        border-color: transparent;
                        border-radius: 5px;

                    }}

                    QCalendarWidget QToolButton{{
                        height:38px;
                        width:50px;
                        color:white;
                        font:18px 'Segoe UI', 'Microsoft YaHei', 'PingFang SC';
                        icon-size:18px 18px;
                        background-color:#2b2b2b;
                    }}
                    QCalendarWidget QToolButton:hover{{
                        background-color:#202020;
                    }}

                    QCalendarWidget QWidget#qt_calendar_navigationbar{{
                        height:35px;
                        background-color:#2b2b2b;

                    }}


                    #qt_calendar_prevmonth,
                    #qt_calendar_nextmonth{{
                        border:none;
                        qproperty-icon:none;
                        background-color:transparent;
                    }}


                    #qt_calendar_prevmonth{{
                        qproperty-icon: url(:/icons/svg_cache/ri_arrow-left-s-line.svg);
                        icon-size: 15px 15px
                    }}

                    #qt_calendar_nextmonth{{
                        qproperty-icon: url(:/icons/svg_cache/ri_arrow-right-s-line.svg);
                        icon-size: 15px 15px
                    }}


                    #qt_calendar_prevmonth:hover,
                    #qt_calendar_nextmonth:hover{{
                        background-color:#202020;
                    }}




                    #qt_calendar_monthbutton{{
                        width:100px;
                        font:18px 'Segoe UI', 'Microsoft YaHei', 'PingFang SC';
                        color:white;
                        background-color:#2b2b2b;
                        margin: 0px 2px;
                        padding: 0px 2px

                    }}

                    #qt_calendar_yearbutton{{
                        font:18px 'Segoe UI', 'Microsoft YaHei', 'PingFang SC';
                        color:white;
                        background-color:#2b2b2b;
                        margin: 0px 2px;
                        padding: 0px 2px

                    }}

                    #qt_calendar_monthbutton:hover,
                    #qt_calendar_yearbutton:hover{{
                        background-color:#202020;
                    }}

                    /* MenuBar Code */

                    QCalendarWidget QMenu{{
                        width:150px;
                        color:white;
                        font:14px 'Segoe UI', 'Microsoft YaHei', 'PingFang SC';
                        background-color:#2b2b2b;
                    }}

                    /* SpinBox Code */



                    /* Calendar View Code */
                    QCalendarWidget QWidget{{
                        alternate-background-color:#2b2b2b;
                    }}


                    QCalendarWidget QAbstractItemView:enabled{{
                        font:14px 'Segoe UI', 'Microsoft YaHei', 'PingFang SC';
                        color:white;
                        background-color:#2b2b2b;
                        selection-background-color:#202020;
                        selection-color:white;
                    }}
                    QCalendarWidget QAbstractItemView:disabled{{
                        color:rgb(100,100,100);
                    }}

                    QCalendarWidget QSpinBox{{
                        width:60px;
                        height:25px;
                        font:14px 'Segoe UI', 'Microsoft YaHei', 'PingFang SC';
                        color:white;
                        background-color:#2b2b2b;
                    }}

                    #qt_calendar_calendarview{{
                        font:14px 'Segoe UI', 'Microsoft YaHei', 'PingFang SC';
                        color:white;
                        background-color:#2b2b2b;
                        border-width: 0px;
                        border-color: #2b2b2b;
                        border-radius:5px;
                    }}


                    #qt_calendar_calendarview::item{{
                        background-color:#2b2b2b;
                        border-width: 0px;
                        border-color: #2b2b2b;
                        border-radius:25px;

                    }}


                    #qt_calendar_calendarview::item:hover{{
                        background-color:#202020;
                        border-width: 0px;
                        border-color: #202020;
                        border-radius:25px;

                    }}

                    #qt_calendar_calendarview::item:selected{{
                        background-color:black;
                        border-width: 0px;
                        border-color: black;
                        border-radius:25px;
                        
                    }}


            """
        )