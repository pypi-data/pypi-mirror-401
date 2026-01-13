from PySide6.QtCore import QEasingCurve

def chooseEasing(ease_data):
    """Choose QEasingCurve from ease_data. If ease_data is a list (bezier),
    fallback to OutCubic for now. If it's a string, attempt to map.
    """
    # if given as list/tuple -> fallback
    if isinstance(ease_data, (list, tuple)):
        return QEasingCurve(QEasingCurve.Type.OutCubic)
    # if string -> try map common ones
    if isinstance(ease_data, str):
        # minimal mapping, extend if needed
        easing_map = {
            'linear': QEasingCurve.Type.Linear,
            'inQuad': QEasingCurve.Type.InQuad,
            'outQuad': QEasingCurve.Type.OutQuad,
            'inOutQuad': QEasingCurve.Type.InOutQuad,
            'outInQuad': QEasingCurve.Type.OutInQuad,
            'inCubic': QEasingCurve.Type.InCubic,
            'outCubic': QEasingCurve.Type.OutCubic,
            'inOutCubic': QEasingCurve.Type.InOutCubic,
            'outInCubic': QEasingCurve.Type.OutInCubic,
            'inQuart': QEasingCurve.Type.InQuart,
            'outQuart': QEasingCurve.Type.OutQuart,
            'inOutQuart': QEasingCurve.Type.InOutQuart,
            'outInQuart': QEasingCurve.Type.OutInQuart,
            'inQuint': QEasingCurve.Type.InQuint,
            'outQuint': QEasingCurve.Type.OutQuint,
            'inOutQuint': QEasingCurve.Type.InOutQuint,
            'outInQuint': QEasingCurve.Type.OutInQuint,
            'inSine': QEasingCurve.Type.InSine,
            'outSine': QEasingCurve.Type.OutSine,
            'inOutSine': QEasingCurve.Type.InOutSine,
            'outInSine': QEasingCurve.Type.OutInSine,
            'inExpo': QEasingCurve.Type.InExpo,
            'outExpo': QEasingCurve.Type.OutExpo,
            'inOutExpo': QEasingCurve.Type.InOutExpo,
            'outInExpo': QEasingCurve.Type.OutInExpo,
            'inCirc': QEasingCurve.Type.InCirc,
            'outCirc': QEasingCurve.Type.OutCirc,
            'inOutCirc': QEasingCurve.Type.InOutCirc,
            'outInCirc': QEasingCurve.Type.OutInCirc,
            'inElastic': QEasingCurve.Type.InElastic,
            'outElastic': QEasingCurve.Type.OutElastic,
            'inOutElastic': QEasingCurve.Type.InOutElastic,
            'outInElastic': QEasingCurve.Type.OutInElastic,
            'inBack': QEasingCurve.Type.InBack,
            'outBack': QEasingCurve.Type.OutBack,
            'inOutBack': QEasingCurve.Type.InOutBack,
            'outInBack': QEasingCurve.Type.OutInBack,
            'inBounce': QEasingCurve.Type.InBounce,
            'outBounce': QEasingCurve.Type.OutBounce,
            'inOutBounce': QEasingCurve.Type.InOutBounce,
            'outInBounce': QEasingCurve.Type.OutInBounce,
            # fallback cho các easing khác
            'sineCurve': QEasingCurve.Type.SineCurve,
            'cosineCurve': QEasingCurve.Type.CosineCurve,
        }
        t = easing_map.get(ease_data, QEasingCurve.Type.OutCubic)
        return QEasingCurve(t)
    # default
    return QEasingCurve(QEasingCurve.Type.OutCubic)

