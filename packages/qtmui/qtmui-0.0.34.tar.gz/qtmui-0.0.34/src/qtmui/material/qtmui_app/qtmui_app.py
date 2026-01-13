from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QThreadPool, QByteArray, Qt
from PySide6.QtGui import QPixmap, QIcon

from qtmui.material.styles import theme_store
from qtmui.hooks.use_routes import router_store

def iconFromBase64(base64):
  pixmap = QPixmap()
  pixmap.loadFromData(QByteArray.fromBase64(base64.encode()))
  icon = QIcon(pixmap)
  return icon

class QtMuiApp(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        icon = iconFromBase64("iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAAAXNSR0IB2cksfwAAAARnQU1BAACxjwv8YQUAAAAgY0hSTQAAeiYAAICEAAD6AAAAgOgAAHUwAADqYAAAOpgAABdwnLpRPAAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAAuIwAALiMBeKU/dgAAAAd0SU1FB+kKCQkiC/WWE+YAAAeiSURBVGjezZp/cFXFFcc/e5OAERxkUgq1KNb6kyq1xRal0iJmkIG2tEqlg/wyt0xbw9QpN8GKyL4rCdW8tzSVQm0n+2wsDrRS+nMCCNjyw1qsdSpqbZlSZQYcGQXUhhZM8rZ/ZF+6ubnvJTE/d+bNu3fP7n3fc/ecs+d89wn6uPlBeD5wntMlgGNayZbeeL7oIbhzgcnAJOAm4ALgaeCIEWa3MOI7wGeB8yNTDwMbgaRW8nS/K+AvCz1TYL4gMuIRYEwPfv8o8DWt5I5+U2BO9T3eiJPnrgPu6sa0NxBswrAAKIn8bgZYYDyzNZ1MnOlTBfwgFMB64JtO91ngoDWdbPs6UAQUZjuMZ6ank4mdfhCWAquAGyO//ybwN+DZpuLmlY9VrX6v1xTwg1AYzBiBWAMsdkRbjWeWpJOJkzFzxhvPzBIZUW2VaTSYi9IqccrK7wJ+kAPDcaAeWNGZs4sugJ8MVANTcwz5F4J0kzi75rHkGtNhfkV4NYZ64JPAT7SSd2ZlZZWJKSIj9ub5+V3AjHxKeHnBV4QpYF8e8ACXYKgqygw95AfhRVGhTsmXgOnA88BtfhCOzMrSycS+iC/tAg4496VAXT6MXp43X48hiIx5F3jc2vh8+7kf2AxcCuzyg3BcByWUPGGEKQU8I7gmIq4DDtnrC7WS1wPPOPLFfhDOyoWzMAf4pcBCp+sk8AhQrZX8T9yc+eGKhUPfHVprFbwxKk+nEqfKKsJFwvA5YK+jXJMfhMuBXwEftd0LgZ3Axfb+IT8Id2glmztdAT8IPwx83+naD9yslbwvF3iAjXJNk1ayHGGW+EF4WazDGZ4CXowRbQdOOEr900a7bPsYcGWXnNgPwruBWnv7HDBZK9nUDynHk0CJVnKi3SwFgiPAhVm9gG9EVyHOhD7lXDcC+/wgnGDvn7Ur8lut5IE+0GN72yqslcYPwu3AkqyOwKhFlavm1CcfaIo1IbtRzXW6pto8pxg4A5xjI0NtWUXC72XwGaAhYh/RFOOLhZmCJ/xl4ZBcKzA1pu8QkDTCbE6nEo19aEXbtJJPt+sxNMeMm208U2aDyv99wK8Ir8fwB2CoM/gh4IF8ztvHfjHbRifszrzIXr8NXKKVPFVoB3oYfuyCN56ZmU4mtjGwLRvNjmQKTLnXIr4EjLDp+TTgF57jIO4GUzMIwAN83H7XPlqTOG2jYrbdAOBZx53nCF7WSt4z0MjvXC6HWFz/sEkfwJ+dIV/NOvE5kVyn1rHBYiubABzVSj7eXwp4Ld69NoBMjduBARMXhZq0knWL7ru/uPBsYTWGeUAJgm9ZB+8v5x0PfBq4SSt53BEVuZbSUQHBJr8inMkZtC0VXwNzqU4ljvSzBZ3USsYlcO7ec6CjAoZpThL3KjBNq34Hj1byjZhVuRIY5rzsY9mduAV43XaPdQb4WsnXGCxNMKudCZnWFy2sdnXtlkewRafkVwYLdusTL0Qs5r/AZR5ApjDzcMSU1g8i8GOAnzngD9vvYmCEB+A1e1Mi8/bEPOgjAwB+tC1srrZFVQXwp7iCZoLTt0kraZyHjPSDcAfwwX4G7wPHLNv3U6BUK6lsNtyhHhgXSWvbwNsc/YU+yv9zgb/ZRpzbjDAN6VSiyfZPB0a7rl3YCb2yDRhvWYX+DKO7gd0xohXO9etayZe9aCVkqT/8inC+LWae10q+MwiceTmtRHG2fc/1gT86ghl+EI7E8G173zDQ4MsqE6WWXMtayqksX1ToFO+HgMvt/XeBa+31ewP41ocBS8mw2sHaRCuj/XbbCljqLhkhZ/ORXlV9DLzED8I7bE38YCSJm6eV3NqhJtZK1vlBeC1Qno87spzPfGBlLwJeRitpnC3WLwDOowPTSgu0z4qjb3kVgrWRvtIoCZeL0etB1FkL3Ar8Evi3NdsTdvP6tTP0oFbyrbzEln0jtcDd9va0EYxJp2Sjlf0FGK2VHNv3PpAQIPYBn7FdSa3k8rzUYmsqZKqcDW0YwpQ54g8Ao/wgvDhG8c/7QXh5jpcyyg/CG7phVleBaHDAAzzaKTcKkFaJt4DftS1TRlSVLU9c4QwZAsyOmfohBLfnMJM3ESz2g3CdH4QleYAXlVUm7sCeDTiiB7WSr3TKjToPugb4q6Pkc3YjecWmHqeBcVrJE86cKcBeI7gqnZJ/j3nmcLtpTrIAn7I279KaM+l4cPgb4Na4gw4vj2O9CPzI6bqOVlr8YJtpQRiZth94VRh2+kF4RcwzG4FbbDk4A6gBfuh8yqLgTWtQ+XKuU5quHDFtoP2hXrRt0EqWOwzfSgyrgaMIFuuU3B27u1Yk5ggjVjrcT7Q9A9yrldyTv1DrmkOV29yjqDMl5tZUFgw/PvxwNsM1wmwQRmzRSv4+jvvxWrz6LMdj2xMW+OGuVZpdjwqjgAXWD6bbishtLwHrMkWZzV6z94kIDWPsZyOtLDc2VZkIFDjjfq6VnNu9Uvn97ZxF1hEbaP8/CIBmu1uOJcepSo62BajsLpHQ0/9KTLK033U9eMxRBDUiI9bXrV2V6T5Z0fM8ZghwO7CU1rNg10/eAfYYYWqEEROtPBudnrRRbb9W8uz7Z1t6c+uvCEdg2oXmJhs6+6z9D6jNpzwIW8fdAAAAAElFTkSuQmCC")
        self.setWindowIcon(icon)
        
        # self.focusChanged.connect(self.focus_changed)
        self.aboutToQuit.connect(self.close_all_widgets)
        self.mainWindow = None  # Khai báo thuộc tính window
        self.threadPool = QThreadPool()  # Khai báo thuộc tính window

    def focus_changed(self, old_widget, new_widget):
        if old_widget:
            print(f"Focus mất khỏi: {old_widget.objectName()}")
        if new_widget:
            print(f"Focus đến: {new_widget.objectName()}")

    def close_all_widgets(self):
        try:
            theme_store.clean_up()
            router_store.clean_up()
            for widget in QApplication.allWidgets():
                if widget.windowFlags() & Qt.Window:  # Kiểm tra nếu widget là cửa sổ độc lập
                    widget.close()
        except Exception as e:
            print(e)
        


