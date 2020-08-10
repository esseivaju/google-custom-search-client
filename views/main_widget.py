from PySide2.QtWidgets import (
    QPushButton, QHBoxLayout, QVBoxLayout,
    QWidget, QPlainTextEdit, QProgressDialog)
from PySide2.QtCore import Slot
from views.query_builder_dialog import QueryBuilderDialog
from views.auth_status_widget import AuthStatusWidget

from PySide2.QtCore import Qt


class MainWidget(QWidget):

    def __init__(self, api_services, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__api_services = api_services
        self.__setup_base()
        self.credentials_update()

    def __setup_base(self):
        self.layout = QVBoxLayout()

        self.dialog = QueryBuilderDialog(slot=self.__add_query)

        self.textEditQuery = QPlainTextEdit()
        self.layout.addWidget(self.textEditQuery)

        self.btn_send = QPushButton("Send queries")
        self.btn_send.clicked.connect(self.__on_send_clicked)
        self.layout.addWidget(self.btn_send)

        self.btn_build_query = QPushButton("Build query")
        self.btn_build_query.clicked.connect(self.__on_build_query_clicked)
        self.layout.addWidget(self.btn_build_query)

        self.auth_widget = AuthStatusWidget(self.__api_services)
        self.layout.addWidget(self.auth_widget)
        self.setLayout(self.layout)

    def setTextContent(self, text):
        self.textEditQuery.setPlainText(text)

    def appendTextContent(self, text):
        current = self.getTextContent()
        if current:
            self.setTextContent(f"{self.getTextContent()}\n{text}")
        else:
            self.setTextContent(text)

    def getTextContent(self):
        return self.textEditQuery.toPlainText()

    def credentials_update(self):
        self.auth_widget.credentials_update()
        self.btn_send.setEnabled(
            self.__api_services.get_customsearch_service().is_configured())

    @Slot()
    def __on_build_query_clicked(self):
        self.dialog = QueryBuilderDialog(slot=self.__add_query)
        self.dialog.show()

    @Slot()
    def __add_query(self, query):
        if query:
            self.appendTextContent(query)
            print(f"Query: {query}")

    @Slot()
    def __on_send_clicked(self):
        self.__active_requests = self.getTextContent().splitlines()

        if not self.__active_requests:
            return

        self.progress_dialog = QProgressDialog(
            "Processing requests...", None,
            0, len(self.__active_requests), self)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.show()
        for line in self.__active_requests:
            self.__api_services.get_customsearch_service().search_qs(
                line, callback=self.__send_callback)
        self.__api_services.get_customsearch_service().flush()

    def __send_callback(self, request_id, response, error):
        import time
        time.sleep(1)
        self.setTextContent(f"{self.getTextContent()}\n{response}")
        completed = max(self.progress_dialog.value(), 0) + 1
        self.progress_dialog.setValue(completed)
