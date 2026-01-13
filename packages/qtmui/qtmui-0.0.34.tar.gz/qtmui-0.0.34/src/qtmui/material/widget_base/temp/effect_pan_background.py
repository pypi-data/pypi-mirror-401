
import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFrame,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from PySide6.QtCore import (
    Qt,
    QObject,
    Property,
    QPropertyAnimation,
    QEasingCurve,
    QPointF,
)
from PySide6.QtGui import QLinearGradient, QColor, QBrush




class BackgroundPanEffect(QObject):
    """
    BackgroundPanEffect "pro"

    - GIỮ chiến lược mượt:
        Gradient rất dài + dịch geometry
    """

    PRESET_COLORS = {
        "ocean": {
            "light": ("#2193b0", "#6dd5ed"),
            "dark": ("#141e30", "#243b55"),
        },
        "sunset": {
            "light": ("#ff512f", "#f09819"),
            "dark": ("#3a1c71", "#d76d77"),
        },
        "forest": {
            "light": ("#11998e", "#38ef7d"),
            "dark": ("#0f2027", "#203a43"),
        },
    }

    def __init__(
        self,
        widget: QWidget,
        variant="panRight",
        colors="ocean",
        interpolate="rgb",
        steps=4,
        duration=10000,
        theme="light",
    ):
        super().__init__(widget)

        self._widget = widget
        self._variant = variant
        self._interpolate = interpolate
        self._steps = max(2, steps)
        self._duration = duration
        self._theme = theme

        self._colors = self._resolve_colors(colors)

        self._offset = 0.0

        self._anim = QPropertyAnimation(self, b"offset", self)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.setDuration(self._duration)
        self._anim.setLoopCount(-1)
        self._anim.setEasingCurve(QEasingCurve.Linear)
        self._anim.start()

    # ---------------- Property ----------------
    def getOffset(self):
        return self._offset

    def setOffset(self, value):
        self._offset = value
        self._apply_gradient()

    offset = Property(float, getOffset, setOffset)

    # ---------------- Resolve colors ----------------
    def _resolve_colors(self, colors):
        if isinstance(colors, str):
            preset = self.PRESET_COLORS.get(colors)
            return preset[self._theme]
        return tuple(colors)

    # ---------------- Generate colors ----------------
    def _generate_colors(self):
        start = QColor(self._colors[0])
        end = QColor(self._colors[1])

        result = []

        for i in range(self._steps):
            t = i / (self._steps - 1)

            if self._interpolate == "hsl":
                c = QColor.fromHsl(
                    int(start.hslHue() + t * (end.hslHue() - start.hslHue())),
                    int(start.hslSaturation() + t * (end.hslSaturation() - start.hslSaturation())),
                    int(start.lightness() + t * (end.lightness() - start.lightness())),
                )
            else:
                c = QColor(
                    int(start.red() + t * (end.red() - start.red())),
                    int(start.green() + t * (end.green() - start.green())),
                    int(start.blue() + t * (end.blue() - start.blue())),
                )

            result.append(c)

        # DEBUG
        # print("[DEBUG] Colors:", [c.name() for c in result])
        return result

    # =====================================================
    # 🔥 FIX MƯỢT Ở ĐÂY – DỊCH GEOMETRY, KHÔNG DỊCH COLOR
    # =====================================================
    def _apply_gradient(self):
        rect = self._widget.rect()
        colors = self._generate_colors()

        fill_factor = 6  # CHÌA KHÓA MƯỢT

        # ---------------- Horizontal ----------------
        if self._variant in ("panRight", "panLeft"):
            fill_w = rect.width() * fill_factor
            grad = QLinearGradient(0, 0, fill_w, 0)

            for i, c in enumerate(colors + [colors[0]]):
                grad.setColorAt(i / len(colors), c)

            pos = self._offset
            if self._variant == "panLeft":
                pos = 1 - pos

            offset = -pos * fill_w
            grad.setStart(offset, 0)
            grad.setFinalStop(offset + fill_w, 0)

        # ---------------- Vertical ----------------
        else:
            fill_h = rect.height() * fill_factor
            grad = QLinearGradient(0, 0, 0, fill_h)

            for i, c in enumerate(colors + [colors[0]]):
                grad.setColorAt(i / len(colors), c)

            pos = self._offset
            if self._variant == "panUp":
                pos = 1 - pos

            offset = -pos * fill_h
            grad.setStart(0, offset)
            grad.setFinalStop(0, offset + fill_h)

        grad.setSpread(QLinearGradient.RepeatSpread)

        # DEBUG chỗ nghi ngờ
        # if abs(self._offset) < 0.01 or abs(self._offset - 1) < 0.01:
        #     print(f"[DEBUG] offset={self._offset:.3f}, start={grad.start()}, end={grad.finalStop()}")

        palette = self._widget.palette()
        palette.setBrush(self._widget.backgroundRole(), QBrush(grad))
        self._widget.setAutoFillBackground(True)
        self._widget.setPalette(palette)






class DemoFrame(QFrame):
    """
    Frame demo dùng để:
    - Hiển thị label mô tả
    - Gắn BackgroundPanEffect
    """

    def __init__(self, title: str, effect_kwargs: dict):
        super().__init__()

        # ==========================
        # Style cơ bản cho frame demo
        # ==========================
        self.setFixedHeight(120)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        # ==========================
        # Layout + label
        # ==========================
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        label = QLabel(title)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(
            """
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            """
        )

        layout.addStretch()
        layout.addWidget(label)
        layout.addStretch()
        
        self.setStyleSheet("background-color: transparent;border: 1px solid red; border-radius: 16px;")

        # ==========================
        # Apply BackgroundPanEffect
        # ==========================
        self._effect = BackgroundPanEffect(
            widget=self,
            **effect_kwargs
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BackgroundPanEffect Demo")
        self.resize(900, 600)

        # =====================================================
        # Central widget là QFrame (đúng yêu cầu)
        # =====================================================
        central = QFrame()
        central.setObjectName("central")
        central.setStyleSheet(
            """
            QFrame#central {
                background-color: #121212;
            }
            """
        )
        self.setCentralWidget(central)

        # =====================================================
        # Layout chính
        # =====================================================
        root_layout = QVBoxLayout(central)
        root_layout.setSpacing(16)
        root_layout.setContentsMargins(24, 24, 24, 24)

        # =====================================================
        # Case 1: Preset colors + panRight + light theme
        # =====================================================
        root_layout.addWidget(
            DemoFrame(
                title='Preset "ocean" | panRight | light',
                effect_kwargs=dict(
                    variant="panRight",
                    colors="ocean",
                    theme="light",
                ),
            )
        )

        # =====================================================
        # Case 2: Preset colors + panLeft + dark theme
        # =====================================================
        root_layout.addWidget(
            DemoFrame(
                title='Preset "sunset" | panLeft | dark',
                effect_kwargs=dict(
                    variant="panLeft",
                    colors="sunset",
                    theme="dark",
                ),
            )
        )

        # =====================================================
        # Case 3: Custom colors + RGB interpolate
        # =====================================================
        root_layout.addWidget(
            DemoFrame(
                title='Custom colors | RGB | panDown',
                effect_kwargs=dict(
                    variant="panDown",
                    colors=("#ee7752", "#23d5ab"),
                    interpolate="rgb",
                    steps=4,
                    theme="light",
                ),
            )
        )

        # =====================================================
        # Case 4: Custom colors + HSL interpolate (mượt hơn)
        # =====================================================
        root_layout.addWidget(
            DemoFrame(
                title='Custom colors | HSL | panUp',
                effect_kwargs=dict(
                    variant="panUp",
                    colors=("#00c6ff", "#0072ff"),
                    interpolate="hsl",
                    steps=6,
                    theme="dark",
                ),
            )
        )

        # =====================================================
        # Case 5: Forest preset + nhiều steps
        # =====================================================
        root_layout.addWidget(
            DemoFrame(
                title='Preset "forest" | panRight | steps=8',
                effect_kwargs=dict(
                    variant="panRight",
                    colors="forest",
                    interpolate="hsl",
                    steps=8,
                    theme="light",
                ),
            )
        )

        root_layout.addStretch()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec())
