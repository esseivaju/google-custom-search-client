import sys

from PySide2.QtWidgets import QApplication
from views.main_window import MainWindow
from services.google_api_service import GoogleAPIsService

if __name__ == "__main__":
    app = QApplication(sys.argv)

    services = GoogleAPIsService()
    window = MainWindow(services)
    window.show()
    sys.exit(app.exec_())
