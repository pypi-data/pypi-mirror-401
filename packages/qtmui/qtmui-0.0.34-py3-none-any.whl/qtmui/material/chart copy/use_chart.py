


from qtmui.material.styles import useTheme

def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def useChart(theme=None, options=None):
    theme = useTheme()
    LABEL_TOTAL = {
        "show": True,
        "label": "Total",
        "color": theme.palette.text.secondary,
        "fontSize": theme.typography.subtitle2.fontSize,
        "fontWeight": theme.typography.subtitle2.fontWeight,
        "lineHeight": theme.typography.subtitle2.lineHeight,
    }

    LABEL_VALUE = {
        "offsetY": 8,
        "color": theme.palette.text.primary,
        "fontSize": theme.typography.h3.fontSize,
        "fontWeight": theme.typography.h3.fontWeight,
        "lineHeight": theme.typography.h3.lineHeight,
    }

    base_options = {
        "colors": [
            theme.palette.primary.main, theme.palette.warning.main,
            theme.palette.info.main, theme.palette.error.main,
            theme.palette.success.main, theme.palette.warning.dark,
            theme.palette.success.darker, theme.palette.info.dark,
            theme.palette.info.darker,
        ],
        "chart": {
            "toolbar": {"show": False},
            "zoom": {"enabled": False},
            "foreColor": theme.palette.text.disabled,
            # "fontFamily": theme.typography.fontFamily,
        },
        "grid": {
            "strokeDashArray": 3,
            "borderColor": theme.palette.divider,
        },
        "plotOptions": {
            "bar": {"borderRadius": 4, "columnWidth": "28%"},
            "pie": {"donut": {"labels": {"show": True, "value": LABEL_VALUE, "total": LABEL_TOTAL}}},
            "radialBar": {"track": {"background": theme.palette.grey._500}}
        },
        "responsive": [
            {"breakpoint": theme.breakpoints.sm, "options": {"plotOptions": {"bar": {"columnWidth": "40%"}}}},
            {"breakpoint": theme.breakpoints.md, "options": {"plotOptions": {"bar": {"columnWidth": "32%"}}}},
        ],
    }
    
    if options is None:
        return base_options
    
    merged_options = merge_dicts(base_options, options)
    return merged_options

# Example Usage
# theme should be imported from your theme module
# chart_config = use_chart(theme, {"chart": {"toolbar": {"show": True}}})
# print(chart_config)
