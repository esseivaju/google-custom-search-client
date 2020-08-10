from PySide2.QtWidgets import (QWidget, QLabel, QVBoxLayout)


class AuthStatusWidget(QWidget):

    def __init__(self, services, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__api_services = services
        self.api_key_label = QLabel(f"ApiKey: {services.get_apikey()}")
        self.search_engine_id_label = QLabel(
            f"Search Engine ID: {services.get_customsearch_service().get_search_engine()}")
        dialog_auth_widget_layout = QVBoxLayout()
        dialog_auth_widget_layout.addWidget(self.api_key_label)
        dialog_auth_widget_layout.addWidget(self.search_engine_id_label)
        self.setLayout(dialog_auth_widget_layout)

    def credentials_update(self):
        self.api_key_label.setText(f"ApiKey: {self.__api_services.get_apikey()}")
        self.search_engine_id_label.setText(f"Search Engine ID: {self.__api_services.get_customsearch_service().get_search_engine()}")
