from dataclasses import dataclass


@dataclass
class TypographyType:
    fontWeight: int
    lineHeight: float
    fontSize: str
    responsiveSizes: dict
    textTransform: str


class TypographyStyle:
    """Lớp để định nghĩa kiểu chữ với các thuộc tính như fontSize, fontWeight, lineHeight."""

    def __init__(self, fontWeight=None, lineHeight=None, fontSize=None, responsiveSizes=None, textTransform=None):
        self.fontWeight = fontWeight or 400
        self.lineHeight = lineHeight
        self.fontSize = fontSize
        self.responsiveSizes = responsiveSizes or {}
        self.textTransform = textTransform or "unset"

    def __repr__(self):
        return f"TypographyStyle(fontWeight={self.fontWeight}, lineHeight={self.lineHeight}, fontSize={self.fontSize})".encode('utf-8').decode('utf-8')
    
    def to_qss_props(self):
        return f"""
        font-weight: {self.fontWeight};
        line-height: {self.lineHeight}em;
        font-size: {self.fontSize};
        """

    def toQFont(self):
        from PySide6.QtGui import QFont

        font = QFont()
        font.setPointSizeF(int(self.fontSize.replace('px', '')))
        font.setWeight(QFont.Weight(self.fontWeight))
        return font

class Typography:
    h1: TypographyType
    h2: TypographyType
    h3: TypographyType
    h4: TypographyType
    h5: TypographyType
    h6: TypographyType
    subtitle1: TypographyType
    subtitle2: TypographyType
    body1: TypographyType
    body2: TypographyType
    caption: TypographyType
    overline: TypographyType
    button: TypographyType

    def __init__(self):
        self.primary_font = "Public Sans, sans-serif"
        self.fontWeightRegular = 400
        self.fontWeightMedium = 500
        self.fontWeightSemiBold = 600
        self.fontWeightBold = 700

        self.h1 = TypographyStyle(
            fontWeight=800,
            lineHeight=80 / 64,
            fontSize=self.int_to_px(40),
            responsiveSizes=self.responsive_font_sizes(sm=52, md=58, lg=64)
        )
        self.h2 = TypographyStyle(
            fontWeight=800,
            lineHeight=64 / 48,
            fontSize=self.int_to_px(32),
            responsiveSizes=self.responsive_font_sizes(sm=40, md=44, lg=48)
        )
        self.h3 = TypographyStyle(
            fontWeight=700,
            lineHeight=1.5,
            fontSize=self.int_to_px(24),
            responsiveSizes=self.responsive_font_sizes(sm=26, md=30, lg=32)
        )
        self.h4 = TypographyStyle(
            fontWeight=700,
            lineHeight=1.5,
            fontSize=self.int_to_px(20),
            responsiveSizes=self.responsive_font_sizes(sm=20, md=24, lg=24)
        )
        self.h5 = TypographyStyle(
            fontWeight=700,
            lineHeight=1.5,
            fontSize=self.int_to_px(18),
            responsiveSizes=self.responsive_font_sizes(sm=19, md=20, lg=20)
        )
        self.h6 = TypographyStyle(
            fontWeight=700,
            lineHeight=28 / 18,
            fontSize=self.int_to_px(17),
            responsiveSizes=self.responsive_font_sizes(sm=18, md=18, lg=18)
        )
        self.subtitle1 = TypographyStyle(
            fontWeight=600,
            lineHeight=1.5,
            fontSize=self.int_to_px(16)
        )
        self.subtitle2 = TypographyStyle(
            fontWeight=600,
            lineHeight=22 / 14,
            fontSize=self.int_to_px(14)
        )
        self.body1 = TypographyStyle(
            lineHeight=1.5,
            fontSize=self.int_to_px(13)
        )
        self.body2 = TypographyStyle(
            lineHeight=22 / 14,
            fontSize=self.int_to_px(12)

        )
        self.caption = TypographyStyle(
            lineHeight=1.5,
            fontSize=self.int_to_px(11)
        )
        self.overline = TypographyStyle(
            fontWeight=700,
            lineHeight=1.5,
            fontSize=self.int_to_px(12),
            textTransform="uppercase"
        )
        self.button = TypographyStyle(
            fontWeight=700,
            lineHeight=24 / 14,
            fontSize=self.int_to_px(12),
            textTransform="unset"
        )

    @staticmethod
    def int_to_px(value: int) -> str:
        return f'{value}px'.encode('utf-8').decode('utf-8')
    
    @staticmethod
    def px_to_rem(value: int) -> str:
        """Chuyển đổi px sang rem."""
        return f"{value / 16}rem".encode('utf-8').decode('utf-8')

    def responsive_font_sizes(self, sm: int, md: int, lg: int) -> dict:
        """Tạo các kích thước phông chữ phản hồi cho các điểm dừng khác nhau."""
        return {
            '@media (min-width:600px)': {
                'fontSize': self.int_to_px(sm),
            },
            '@media (min-width:900px)': {
                'fontSize': self.int_to_px(md),
            },
            '@media (min-width:1200px)': {
                'fontSize': self.int_to_px(lg),
            },
        }



# # Sử dụng lớp Typography
# typography = Typography()

# # Truy xuất fontSize của h3
# print(typography.h3.fontSize)  # Trả về "1.5rem"
# print(typography.h3.fontWeight)  # Trả về "700"
