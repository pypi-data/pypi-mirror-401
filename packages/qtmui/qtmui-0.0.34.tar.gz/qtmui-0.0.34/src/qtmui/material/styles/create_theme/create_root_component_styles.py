from functools import reduce
from copy import deepcopy

# Import các thành phần tương tự từ các tệp liên quan
from .default_props import default_props
from .components.input_base import input_base
from .components.fab import fab
from .components.card import card
from .components.chip import chip
from .components.tabs import tabs
from .components.menu import menu
from .components.list import list
from .components.table import table
from .components.alert import alert
from .components.avatar import avatar
from .components.badge import badge
from .components.box import box
from .components.paper import paper
from .components.radio import radio
from .components.container import container
# from .components.appbar import appBar
from .components.drawer import drawer
from .components.dialog import dialog
from .components.masonry import masonry
from .components.grid import grid
from .components.rating import rating
from .components.slider import slider
from .components.stepper import stepper
from .components.button import button
from .components.select import select
from .components.switch import switch
from .components.tooltip import tooltip
# from .components.stepper import stepper
# from .components.svg_icon import svg_icon
from .components.skeleton import skeleton
# from .components.backdrop import backdrop
from .components.progress import progress
from .components.timeline import timeline
from .components.checkbox import checkbox
# from .components.data_grid import data_grid
from .components.tree_view import tree_view
from .components.textfield import text_field
from .components.accordion import accordion
from .components.typography import typography
from .components.pagination import pagination
from .components.label import label
from .components.group_box import group_box
from .components.popover import popover
from .components.snackbar import snackbar
# from .components.date_picker import date_picker
from .components.breadcrumbs import breadcrumbs
# from .components.css_baseline import css_baseline
from .components.button_group import button_group
from .components.autocomplete import autocomplete
from .components.toggle_button import toggle_button
from .components.loading_button import loading_button
from .components.text_max_line import text_max_line
from .components.stack import stack
from .components.splitter import splitter
from .components.title_bar import title_bar
from .components.upload import upload

from .components.textfields.py_combo_box import py_combo_box
from .components.textfields.py_date_edit import py_date_edit
from .components.textfields.py_date_time_edit import py_date_time_edit
from .components.textfields.py_dial import py_dial
from .components.textfields.py_double_spin_box import py_double_spin_box
from .components.textfields.py_filled_input import py_filled_input
from .components.textfields.py_font_combo_box import py_font_combo_box
from .components.textfields.py_input import py_input
from .components.textfields.py_line_edit import py_line_edit
from .components.textfields.py_plain_text_edit import py_plain_text_edit
from .components.textfields.py_spin_box import py_spin_box
from .components.textfields.py_text_edit import py_text_edit
from .components.textfields.py_time_edit import py_time_edit

from .components.textfields.py_outlined_input import py_outlined_input
from .components.textfields.py_filled_input import py_filled_input
from .components.textfields.py_standard_input import py_standard_input

from .components.py_tool_button import py_tool_button
from .components.py_svg_widget import py_svg_widget

from ....utils.data import merge_dicts


# Hàm chính tương tự với 'componentsOverrides' trong JavaScript
def create_root_component_styles(theme):
    # print('vao000000day____________________')
    components = merge_dicts(
        default_props(theme),
        fab(theme),
        input_base(theme),
        tabs(theme),
        chip(theme),
        card(theme),
        menu(theme),
        list(theme),
        box(theme),
        badge(theme),
        table(theme),
        paper(theme),
        alert(theme),
        avatar(theme),
        radio(theme),
        select(theme),
        button(theme),
        container(theme),
        rating(theme),
        dialog(theme),
        masonry(theme),
        grid(theme),
        # appBar(theme),
        slider(theme),
        stepper(theme),
        drawer(theme),
        # stepper(theme),
        tooltip(theme),
        # svg_icon(theme),
        switch(theme),
        snackbar(theme),
        checkbox(theme),
        # data_grid(theme),
        skeleton(theme),
        timeline(theme),
        tree_view(theme),
        # backdrop(theme),
        progress(theme),
        text_field(theme),
        accordion(theme),
        typography(theme),
        pagination(theme),
        label(theme),
        group_box(theme),
        popover(theme),
        # date_picker(theme),
        button_group(theme),
        breadcrumbs(theme),
        # css_baseline(theme),
        autocomplete(theme),
        toggle_button(theme),
        loading_button(theme),
        text_max_line(theme),
        stack(theme),
        splitter(theme),
        title_bar(theme),
        upload(theme),

        py_combo_box(theme),
        py_date_edit(theme),
        py_date_time_edit(theme),
        py_dial(theme),
        py_double_spin_box(theme),
        py_font_combo_box(theme),
        py_input(theme),
        py_line_edit(theme),
        py_plain_text_edit(theme),
        py_spin_box(theme),
        py_text_edit(theme),
        py_time_edit(theme),

        py_outlined_input(theme),
        py_filled_input(theme),
        py_standard_input(theme),
        
        py_tool_button(theme),
        py_svg_widget(theme),

    )
    return components
