from PySide2.QtWidgets import (QMainWindow,
                               QAction, QInputDialog, QDialog, QVBoxLayout, QLabel, QWidget, QErrorMessage,
                               QLineEdit, QFileDialog, QApplication)
from PySide2.QtGui import QKeySequence
from PySide2.QtCore import Slot
from views.main_widget import MainWidget
from views.auth_status_widget import AuthStatusWidget
from pathlib import Path
import os


class MainWindow(QMainWindow):

    def __init__(self, services, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert services is not None
        self.__api_services = services
        self.__setup_base()
        self.__auth_path = Path.home().joinpath(".nb_crawler_auth")
        self.__generate_menu()

    def __setup_base(self):
        centralWidget = MainWidget(self.__api_services)
        self.setCentralWidget(centralWidget)
        screen_size = QApplication.instance().primaryScreen().size()
        self.resize(screen_size.width(), screen_size.height())

    def __input_dialog(self, title, text):
        key, ok = QInputDialog().getText(self, title, text, QLineEdit.Normal)
        if ok:
            return key
        return None

    @Slot()
    def __register_api_key(self):
        key = self.__input_dialog("Register APIKEY", "Key: ")
        if key:
            try:
                self.__api_services.register_apikey(key)
            except Exception as e:
                error_message = QErrorMessage(self)
                if e.args:
                    error_message.showMessage(f"{e.args[0]}")
                else:
                    error_message.showMessage("Unable to configure APIKEY")
            else:
                self.centralWidget().credentials_update()

    @Slot()
    def __register_search_engine_id(self):
        key = self.__input_dialog("Register Search Engine ID", "ID: ")
        if key:
            self.__api_services.get_customsearch_service().register_search_engine(key)
            self.centralWidget().credentials_update()

    @Slot()
    def __load_query_file(self):
        file = QFileDialog().getOpenFileName(self, "Select query file")[0]
        if os.path.exists(file):
            with open(file) as f:
                data = f.read()
                self.centralWidget().setTextContent(data)

    @Slot()
    def __save_query_file(self):
        file = QFileDialog().getSaveFileName(self, "Select file to save")[0]
        with open(file, 'w') as f:
            data = self.centralWidget().getTextContent()
            f.write(data)

    @Slot()
    def __check_auth_status(self):
        dialog_auth = QDialog(self)
        dialog_auth.setModal(True)
        dialog_auth.setWindowTitle("Authentication Keys")

        dialog_auth_widget = AuthStatusWidget(self.__api_services)

        dialogLayout = QVBoxLayout()
        dialogLayout.addWidget(dialog_auth_widget)
        dialog_auth.setLayout(dialogLayout)
        dialog_auth.show()

    def __generate_menu(self):
        self.menu = self.menuBar()

        self.file_menu = self.menu.addMenu("&File")

        # Exit QAction
        open_action = QAction("&Open query file", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.__load_query_file)
        self.file_menu.addAction(open_action)

        save_action = QAction("&Save query file", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.__save_query_file)
        self.file_menu.addAction(save_action)

        self.apiAuthMenu = self.menu.addMenu("&Google APIs")

        apiKeyAction = QAction("&Register APIKEY", self)
        apiKeyAction.setStatusTip("Register APIKEY for customsearch api")
        apiKeyAction.triggered.connect(self.__register_api_key)
        self.apiAuthMenu.addAction(apiKeyAction)

        contextIDAction = QAction("&Register Custom Search Engine", self)
        contextIDAction.setStatusTip(
            "Register Cutom Search Engine for customsearch api")
        contextIDAction.triggered.connect(self.__register_search_engine_id)
        self.apiAuthMenu.addAction(contextIDAction)

        authStatusAction = QAction("&Auth Status", self)
        authStatusAction.setStatusTip(
            "Check authentication status")
        authStatusAction.triggered.connect(self.__check_auth_status)
        self.apiAuthMenu.addAction(authStatusAction)
