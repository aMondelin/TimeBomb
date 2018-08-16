import sys
from PySide.QtGui import *
from timebomb.ui import connection_ui


def generate_ui():
    app = QApplication(sys.argv)
    main_ui = connection_ui.ConnectionUi()
    sys.exit(app.exec_())


if __name__ == "__main__":
    generate_ui()
