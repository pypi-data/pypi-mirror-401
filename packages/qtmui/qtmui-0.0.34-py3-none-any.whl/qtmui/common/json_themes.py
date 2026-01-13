# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and ..site_packages.qtcompat
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
import json
import os

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from .json_settings import Settings

# APP THEMES
# ///////////////////////////////////////////////////////////////
class Themes(object):
    # LOAD SETTINGS
    # ///////////////////////////////////////////////////////////////
    setup_settings = Settings()
    _settings = setup_settings.items

    # APP PATH
    # ///////////////////////////////////////////////////////////////
    json_file = f"src/themes/{_settings['theme_name']}.json"
    app_path = os.path.abspath(os.getcwd())
    settings_path = os.path.normpath(os.path.join(app_path, json_file))
    if not os.path.isfile(settings_path):
        print(f"WARNING: \"gui/themes/{_settings['theme_name']}.json\" not found! check in the folder {settings_path}")

    # INIT SETTINGS
    # ///////////////////////////////////////////////////////////////
    def __init__(self):
        super(Themes, self).__init__()

        # DICTIONARY WITH SETTINGS
        self.items = {}

        # DESERIALIZE
        self.deserialize()

    # SERIALIZE JSON
    # ///////////////////////////////////////////////////////////////
    def serialize(self):
        # WRITE JSON FILE
        with open(self.settings_path, "w", encoding='utf-8') as write:
            json.dump(self.items, write, indent=4)

    # DESERIALIZE JSON
    # ///////////////////////////////////////////////////////////////
    def deserialize(self):
        self.items = {
            "app_name": "PyOneDark - Modern GUI",
            "version" : "v1.0.0",
            "copyright" : "By: Wanderson M. Pimenta",
            "year" : 2021,
            "theme_name" : "bright_theme",
            "custom_title_bar": True,
            "startup_size": [
                1400,
                720
            ],
            "minimum_size": [
                960,
                540
            ],
            "lef_menu_size" : {
                "minimum" : 50,
                "maximum" : 240
            },
            "left_menu_content_margins" : 3,
            "left_column_size" : {
                "minimum" : 0,
                "maximum" : 240
            },
            "right_column_size" : {
                "minimum" : 0,
                "maximum" : 240
            },
            "time_animation" : 500,
            "font" : {
                "family" : "Segoe UI",
                "title_size" : 10,
                "text_size" : 9
            }
        }