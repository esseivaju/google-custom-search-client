from PySide2.QtWidgets import (
    QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QWidget, QPlainTextEdit, QComboBox, QLineEdit, QErrorMessage)
from PySide2.QtCore import Qt
from PySide2.QtCore import Slot


class QueryFormItemWidget(QWidget):

    def __init__(self, label_text, field_key, required=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__label_text = label_text
        self.__field_key = field_key
        self.__req = required
        self.__setup_base()

    def __setup_base(self):
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignRight)
        self.item_label = QLabel(f"{self.__label_text}: ")
        self.item_input = QLineEdit()
        self.layout.addWidget(self.item_label)
        self.layout.addWidget(self.item_input)
        self.setLayout(self.layout)

    def __str__(self):
        return self.get_query_param()

    def is_required(self):
        return self.__req

    def get_field_name(self):
        return self.__label_text

    def get_query_param(self):
        text = self.item_input.text()
        if not text:
            return None
        return f"{self.__field_key}={text}"


class QueryBuilderWidget(QWidget):

    def __init__(self, slot=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__widget_slot = slot
        self.__setup_base()

    def __setup_base(self):
        self.layout = QVBoxLayout()
        self.form_fields = list()
        self.required = list()
        self.__add_form_field(QueryFormItemWidget("Query", "q", required=True))
        self.__add_form_field(QueryFormItemWidget("Phrase", "exactTerms"))

        self.btnDone = QPushButton("Add")
        self.btnDone.clicked.connect(self.add_query_string)
        self.layout.addWidget(self.btnDone)
        self.setLayout(self.layout)

    @Slot()
    def add_query_string(self):
        qs = self.build_query_string()
        ok = True
        missing = ""
        for req in self.required:
            if not req.get_query_param():
                missing = f"{missing} - {req.get_field_name()}"
                ok = False
        if not ok:
            QErrorMessage(self).showMessage(f"Fields required: {missing}")
        else:
            self.parent().accept()
            self.__widget_slot(qs)

    def __add_form_field(self, form_item):
        self.form_fields.append(form_item)
        self.layout.addWidget(form_item)
        if form_item.is_required():
            self.required.append(form_item)

    def build_query_string(self):
        qs = ""
        for form_item in self.form_fields:
            param = form_item.get_query_param()
            if not param:
                continue
            sep = "&" if qs else ""
            qs = f"{qs}{sep}{param}"
        return qs

    def __str__(self):
        return self.build_query_string()
