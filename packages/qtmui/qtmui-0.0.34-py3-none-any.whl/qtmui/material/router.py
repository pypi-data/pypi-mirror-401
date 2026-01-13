# from functools import lru_cache
# import time

# from PySide6.QtWidgets import QStackedWidget, QPushButton
# from PySide6.QtCore import Signal


# from qtmui.material.skeleton import Skeleton
# from qtmui.material.box import Box
# from qtmui.hooks.use_routes import useRouter


# from src.sections._examples.mui.grid_view import GridView
# from src.sections._examples.foundation.colors_view import ColorsView
# # from src.sections._examples.foundation.icons_view import IconsView
# from src.sections._examples.mui.typography_view import TypographyView
# from src.sections._examples.foundation.shadows_view import ShadowsView

# from src.sections._examples.mui.textfield_view import TextFieldView
# from src.sections._examples.mui.button_view.index import ButtonsView

# from src.sections._examples.mui.accordion_view import AccordionView
# from src.sections._examples.mui.breadcrumbs_view import BreadcrumbsView
# from src.sections._examples.mui.data_grid_view.index import DataGridView
# from src.sections._examples.mui.textfield_view import TextFieldView
# from src.sections._examples.mui.autocomplete_view import AutocompleteView
# from src.sections._examples.mui.radio_button_view import RadioButtonView
# from src.sections._examples.mui.checkbox_view import CheckboxView
# from src.sections._examples.mui.switch_view import SwitchView
# from src.sections._examples.mui.alert_view import AlertView
# from src.sections._examples.mui.chip_view import ChipView
# from src.sections._examples.mui.avatar_view import AvatarView
# from src.sections._examples.mui.badge_view import BadgeView
# from src.sections._examples.mui.skeleton_view import SkeletonView
# from src.sections._examples.mui.progress_view import ProgressView
# from src.sections._examples.mui.tabs_view import TabsView
# from src.sections._examples.mui.table_view.index import BasicTableView
# from src.sections._examples.mui.rating_view import RatingView
# from src.sections._examples.mui.dialog_view import DialogView


# from src.sections._examples.extra.snackbar_view import SnackbarView
# from src.sections._examples.extra.navigation_bar_view import NavigationBarView
# from src.sections._examples.extra.upload_view import UploadView


# class Router(QStackedWidget):
#     render_layout = Signal(str)

#     redux_to_main_thread = Signal(str)

#     setVisibleLoadingDialogSignal = Signal(bool)

#     def __init__(self):
#         super().__init__()
        
#         self.map_path_renders:dict[str:object] = {}

#         self.redux_to_main_thread.connect(self.handle_path)

#         # self._process = CircularProgress(self._context)

#         # LoadingDialog(parent=self, setVisibleSignal=self.setVisibleLoadingDialogSignal)
#         # self.setVisibleLoadingDialogSignal.emit(False)

#         # self.render_layout.connect(self.render,Qt.ConnectionType.QueuedConnection)
#         # self.render(path="/components/mui/buttons")
#         self.initUI()
#         # self.render(path="/components/mui/autocomplete")
#         # self.render(path="/dashboard/profile")
#         # self.render(path="/components/extra/navigation-bar")
#         # self.render(path="/components/extra/formValidation")
#         self.render(path="/dashboard/components")

#     def resizeEvent(self, e):
#         super().resizeEvent(e)
#         self.resize(self.width(), self.height())

#     def initUI(self):
#         self.layout().setContentsMargins(0,0,0,0)
#         lazy_wg = Box(
#                 backgroundColor="green",
#                     children=[
#                         Skeleton(variant="text"),
#                         Skeleton(variant="circular"),
#                         Skeleton(variant="rectangular"),
#                         Skeleton(variant="rounded"),
#                     ]
#                 )
        
#         btn = QPushButton('ik')
#         btn.setParent(self)
#         btn.setMinimumHeight(100)
#         btn.setStyleSheet('background: red;')
#         self.map_path_renders["loading_lazy"] = btn
#         self.addWidget(btn)



#     def handle_path(self, path):
#         # self.lazy_wg = Box(
#         #         backgroundColor="green",
#         #             children=[
#         #                 Skeleton(variant="text"),
#         #                 Skeleton(variant="circular"),
#         #                 Skeleton(variant="rectangular"),
#         #                 Skeleton(variant="rounded"),
#         #             ]
#         #         )
#         # self.addWidget(self.lazy_wg)
#         # self.setCurrentWidget(self.lazy_wg)

#         # self._process.run_process(True)


#         self.start_render(path)
        

#     def render(self, path):
#         try:
#             # self.setVisibleLoadingDialogSignal.emit(True)
#             self.redux_to_main_thread.emit(path)

#             # wk = TestWorker(self.start_render,path)
#             # wk.signal.widget_rendered.connect(self.add_widget,Qt.ConnectionType.AutoConnection) # QueuedConnection
#             # wk.start()
            
#         except Exception as e:
#             import traceback
#             traceback.print_exc()

#     def add_widget(self,path,_route):
#         route = self.map_path_renders.get(path)
#         if route == None:
#             route = _route['layout'](page=_route['element']())
#             self.map_path_renders[path]=route
#             self.addWidget(route)
#         self.setCurrentWidget(route)

#         # self.setVisibleLoadingDialogSignal.emit(False)
#         # self._process.run_process(False)


        
#     def start_render(self,path):
#         route = self.map_path_renders.get(path)
#         if route == None:
#             route = self._render(path)
#         self.add_widget(path, route)

#     @lru_cache(maxsize=128)
#     def _render(self,path):
#         # print('lru________________________', path)
#         route = self.get_route(path)
#         return route

#     def clear_layout(self):
#         # Xóa tất cả các phần tử của layout
#         while self.layout().count():
#             child = self.layout().takeAt(0)
#             if child.widget():
#                 child.widget().deleteLater()

#     def get_route(self, path):

#         return useRouter(
#             # _list = [
#             #     {
#             #         'path': '/',
#             #         'element': """(
#             #             <MainLayout>
#             #             <HomePage />
#             #             </MainLayout>
#             #         )"""
#             #     },
#             #     *componentsRoutes,
#             #     # *dashboardRoutes,
#             #     # *mainRoutes,
#             #     { 'path': '*', 'element': 'Navigate(to="/404", replace=True)'  }
#             # ],
#             # route="/components/mui/buttons"
#             # route="/components/extra/form_validation"
#             # route="/components/extra/textfield"
#             # route="/components/mui/autocomplete"
#             path=path
#             # route="/components/mui/stack"
#             # route="/components/mui/table"
#         )
