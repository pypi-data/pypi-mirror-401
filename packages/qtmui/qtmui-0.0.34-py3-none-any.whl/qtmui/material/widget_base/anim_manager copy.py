import asyncio
from typing import Optional, List, Callable, Union

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QScrollArea

from .anim_controller import AnimationController

from qtmui.hooks import State


class AnimManager:
    def __init__(
        self,
        **kwargs,
    ):

        self.initial = kwargs.get("initial", {})
        self.animate = kwargs.get("animate", {})
        self.exit = kwargs.get("exit", {})
        self.variants = kwargs.get("variants", {})
        self.src = kwargs.get("src", None)
        
        if isinstance(self.variants, State):
            self.variants.valueChanged.connect(self.on_variants_changed)
        
        self.children_widgets: List[QWidget] = []
        self.child_controllers: List[AnimationController] = []

        # mark whether we've scheduled children animations already
        self._children_scheduled = False
        self._connected = False

    def on_variants_changed(self, new_variants):
        if self.parent() and hasattr(self.parent(), "child_controllers"):
            for ctl in self.parent().child_controllers:
                ctl.variants = new_variants
                ctl._played = False

            if self.parent().children_widgets:
                QTimer.singleShot(0, self.parent()._children_animation)

    def _children_animation(self):
        self._schedule_children_animation_task = asyncio.ensure_future(self._schedule_children_animation())
        
    def _children_apply_initial(self, fn):
        self._schedule_children_apply_initial_task = asyncio.ensure_future(fn())


    def setup_child(self, child: QWidget = None):
        """Setup children widgets and their AnimationController controllers."""
        self.children_widgets.append(child)
        child_variants = child.getVariants() if hasattr(child, "getVariants") else {}
        child_ctrl = AnimationController(child, child_variants)
        self.child_controllers.append(child_ctrl)
        
    def getVariants(self) -> dict:
        """Get variant definition by name."""
        variant = {}
        if isinstance(self.variants, State):
            variant = self.variants.value
        elif isinstance(self.variants, dict):
            variant = self.variants
        return variant

    def find_scroll_area(self) -> Optional[QScrollArea]:
        p = self.parentWidget()
        while p:
            if isinstance(p, QScrollArea):  # Hoặc isinstance(p, Scrollbar) nếu Scrollbar kế thừa QScrollArea
                return p
            p = p.parentWidget()
        return None

    async def _schedule_children_animation(self):
        try:
            """Apply initial state for all children and then play them with stagger/delay from this Box variants."""
            # # Áp dụng initial cho tất cả children trước
            for ctrl in self.child_controllers:
                ctrl.apply_initial()

            # Kiểm tra nếu container nằm trong QScrollArea (Scrollbar giả sử là subclass của QScrollArea)
            scroll_area = self.find_scroll_area()
            
            if scroll_area:
                # Kết nối signal nếu chưa
                if not self._connected:
                    scroll_area.verticalScrollBar().valueChanged.connect(self._animate_visible_children)
                    self._connected = True
                # Trigger initial animation cho các child visible ban đầu, 100 để các child setStyleSheet xong và có height
                QTimer.singleShot(0, lambda: self._animate_visible_children(scroll_area.verticalScrollBar().value()))
            else:
                # Không có scroll, play tất cả với stagger như cũ
                animate_def = self.getVariants().get("animate", {}) or {}
                transition = animate_def.get("transition", {}) or {}
                base_delay = int(transition.get("delayChildren", 0) * 1000)
                stagger = int(transition.get("staggerChildren", 0) * 1000)
                for idx, ctrl in enumerate(self.child_controllers):
                    delay_ms = base_delay + idx * stagger
                    ctrl.play(delay_ms=delay_ms)
        except Exception as e:
            pass

    def _animate_visible_children(self, scroll_pos: int):
        scroll_area = self.find_scroll_area()
        if not scroll_area:
            return

        viewport_h = scroll_area.viewport().height()
        
        visible_to_play = []
        for idx, ctrl in enumerate(self.child_controllers):
            if ctrl._played:
                continue
            child = self.children_widgets[idx]
            child_y = child.pos().y()  # Vị trí y tương đối với container
            child_h = child.height()
            # Kiểm tra nếu child nằm trong vùng visible (có overlap với viewport)
            if (child_y < scroll_pos + viewport_h) and (child_y + child_h > scroll_pos):
                visible_to_play.append((idx, ctrl))

        if not visible_to_play:
            return

        # Sắp xếp theo thứ tự index để giữ order
        visible_to_play.sort(key=lambda x: x[0])

        # Lấy transition để áp dụng stagger cho batch visible này
        animate_def = self.getVariants().get("animate", {}) or {}
        transition = animate_def.get("transition", {}) or {}
        stagger = transition.get("staggerChildren", 0)
        stagger_ms = int(stagger * 1000) if stagger < 100 else int(stagger)
        # Không dùng delayChildren cho các batch sau, chỉ stagger nội bộ batch
        delay_ms = 0

        for _, ctrl in visible_to_play:
            ctrl.play(delay_ms=delay_ms)
            delay_ms += stagger_ms


    def _runAnimation(self):
        # We must schedule apply_initial and play AFTER layout has assigned positions.
        # Use singleShot(0) to run after the event loop processes layout.
        if self.children_widgets and not self._children_scheduled:
            QTimer.singleShot(0, self._children_animation)
            self._children_scheduled = True
        elif self.variants and not hasattr(self.parent(), "variants"): # kiểm tra rằng parrent có variants = {} => không nhận kiểm soát animation từ parent
            self.animCtl = AnimationController(self, self.getVariants())
            self.animCtl.apply_initial()
            self.animCtl.play(delay_ms=50)
        elif self.variants != {} and (hasattr(self.parent(), "variants") and self.parent().variants == {}): # kiểm tra rằng parrent có variants = {} => không nhận kiểm soát animation từ parent
            self.animCtl = AnimationController(self, self.getVariants())
            self.animCtl.apply_initial()
            QTimer.singleShot(0, self._animCtlPlayTask)
            
        # self._scaleX
            
            
    def _animCtlPlayTask(self):
        self._schedule__animCtlPlayTask = asyncio.ensure_future(self._animCtlPlay())
            
    async def _animCtlPlay(self):
        self.animCtl.play(delay_ms=0)
            
    def showEvent(self, event):
        QTimer.singleShot(0, self._runAnimation)