from PySide2.QtWidgets import (
    QPushButton, QHBoxLayout, QWidget, QPlainTextEdit, QComboBox, QDialog)
from views.query_builder_widget import QueryBuilderWidget


class QueryBuilderDialog(QDialog):

    def __init__(self, slot=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__widget_slot = slot
        self.__setup_base()

    def __setup_base(self):
        self.setWindowTitle("Build custom query")
        self.setModal(True)
        queryBuilderWidget = QueryBuilderWidget(
            parent=self, slot=self.__widget_slot)
        dialogLayout = QHBoxLayout()
        dialogLayout.addWidget(queryBuilderWidget)
        self.setLayout(dialogLayout)
