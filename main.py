import logging
from PyQt6.QtWidgets import QApplication

from main_window import MainWindow

import sys

SINGLA_GUI_VERSION = "1.0"

logging.basicConfig(format="%(threadName)s:%(message)s")
logging.getLogger().setLevel(logging.INFO)




def main():
    """
    The main function for the app. Creates an QApplication and shows the main window.
    """
    app = QApplication(sys.argv)
    main_window = MainWindow()
    app.aboutToQuit.connect(main_window.control.shutdown)
    main_window.show()
    app.exec()


def get_about_info():
    return f"""Singla GUI
Version {SINGLA_GUI_VERSION} 
           
A graphical user interface that synchronizes measurement operations on the TEM microscope with the SINGLA detector"""


if __name__ == '__main__':
    main()
