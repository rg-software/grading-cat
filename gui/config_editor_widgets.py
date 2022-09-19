from abc import abstractmethod
from typing import Union

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QScrollArea
from PySide6.QtWidgets import QLineEdit, QComboBox, QPushButton, QWidget


class UserInputWidget(QWidget):
    """Abstraction for user input fields."""

    def __init__(self, object_name: str):
        super().__init__(objectName=object_name)

    @abstractmethod
    def display_value(self, value: Union[str, list[str]]) -> None:
        ...

    @abstractmethod
    def get_value(self) -> Union[str, list[str]]:
        ...


class SingleLineInputWidget(UserInputWidget):
    def __init__(self, object_name: str, tooltip: str) -> None:
        super().__init__(object_name=object_name)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self._line_edit = QLineEdit(self, toolTip=tooltip)
        layout.addWidget(self._line_edit)
        self.setLayout(layout)

    def display_value(self, value: str) -> None:
        self._line_edit.setText(value)

    def get_value(self) -> Union[str, list[str]]:
        return self._line_edit.text()


class SingleDropdownWidget(UserInputWidget):
    def __init__(self, object_name: str, tooltip: str, options: list) -> None:
        super().__init__(object_name=object_name)

        self.tooltip = tooltip
        self.options = options
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        cb = QComboBox(self, toolTip=tooltip, editable=True)
        cb.addItems(self.options)
        self._line_edit = cb
        layout.addWidget(self._line_edit)
        self.setLayout(layout)

    def display_value(self, value: str) -> None:
        self._line_edit.setEditText(value)

    def get_value(self) -> Union[str, list[str]]:
        return self._line_edit.currentText()


class MultilineWidget(UserInputWidget):
    """
    Structure:
    - MultiLineWidget
        - QScrollArea
            - QWidget
                - QGridLayout
                    - Widget used in create_input()
                    - QPushButton
    """

    BUTTON_ADD_TEXT = "Add"
    BUTTON_ADD_TOOLTIP = "Add new line"
    BUTTON_REMOVE_TEXT = "-"
    BUTTON_REMOVE_TOOLTIP = "Remove line"
    BUTTON_MAX_WIDTH = 50
    REMOVE_BUTTON_MAX_WIDTH = 20
    ROW_FIXED_HEIGHT = 20

    def __init__(self, object_name: str) -> None:
        super().__init__(object_name=object_name)
        self.elements = []

        add_button = QPushButton(
            text=self.BUTTON_ADD_TEXT,
            toolTip=self.BUTTON_ADD_TOOLTIP,
            fixedHeight=self.ROW_FIXED_HEIGHT,
            maximumWidth=self.BUTTON_MAX_WIDTH,
        )
        add_button.clicked.connect(self.add_row)
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addStretch()  # left-align

        self.grid_layout = QGridLayout(verticalSpacing=10)
        self.grid_layout.setColumnMinimumWidth(0, 110)
        self.grid_layout.setColumnMinimumWidth(1, 25)
        # self.add_row()

        vbox_layout = QVBoxLayout()
        vbox_layout.addLayout(self.grid_layout)
        vbox_layout.addLayout(button_layout)

        scrollable_widget = QScrollArea(
            widget=QWidget(layout=vbox_layout),
            widgetResizable=True,
            verticalScrollBarPolicy=Qt.ScrollBarAlwaysOn,
            horizontalScrollBarPolicy=Qt.ScrollBarAlwaysOff,
        )

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scrollable_widget)

        self.setLayout(main_layout)

    @abstractmethod
    def create_input(self) -> QWidget:
        ...

    def destroy_input(self, widget) -> None:
        if widget in self.elements:
            self.elements.pop(self.elements.index(widget))

    def add_row(self) -> None:
        rows = self.grid_layout.rowCount()
        columns = self.grid_layout.columnCount()

        line = self.create_input()
        self.grid_layout.addWidget(line, rows, 0)

        button = QPushButton(
            text=self.BUTTON_REMOVE_TEXT,
            toolTip=self.BUTTON_REMOVE_TOOLTIP,
            fixedHeight=self.ROW_FIXED_HEIGHT,
            maximumWidth=self.REMOVE_BUTTON_MAX_WIDTH,
        )
        # to specify which button is clicked
        # ref: https://stackoverflow.com/a/20334117/5517838
        button.clicked.connect(lambda: self.delete_row(button))

        self.grid_layout.addWidget(button, rows, columns - 1)

    def delete_row(self, button_clicked: QPushButton) -> None:
        index = self.grid_layout.indexOf(button_clicked)
        row = self.grid_layout.getItemPosition(index)[0]
        for column in range(self.grid_layout.columnCount()):
            if layout := self.grid_layout.itemAtPosition(row, column):
                self.destroy_input(layout.widget())
                layout.widget().deleteLater()
                self.grid_layout.removeItem(layout)


class MultilineInputWidget(MultilineWidget):
    def __init__(self, object_name: str, tooltip: str) -> None:
        self.tooltip = tooltip
        self.elements = []
        super().__init__(object_name=object_name)

    def create_input(self) -> QLineEdit:
        e = QLineEdit(toolTip=self.tooltip, fixedHeight=self.ROW_FIXED_HEIGHT)
        self.elements.append(e)
        return e

    def display_value(self, values: list[str]) -> None:
        while len(self.elements) < len(values):
            self.add_row()

        for line, values in zip(self.elements, values):
            line.setText(values)

    def get_value(self) -> list[str]:
        return list({line.text() for line in self.elements})  # prevent duplicates


class MultiDropdownWidget(MultilineWidget):
    def __init__(self, object_name: str, tooltip: str, options: list) -> None:
        self.tooltip = tooltip
        self.options = options
        self.elements = []
        super().__init__(object_name=object_name)

    def create_input(self) -> QComboBox:
        cb = QComboBox(toolTip=self.tooltip, editable=True)
        cb.addItems(self.options)
        cb.setEditText("")
        self.elements.append(cb)
        return cb

    def display_value(self, values: list[str]) -> None:
        while len(self.elements) < len(values):
            self.add_row()

        for dropdown, value in zip(self.elements, values):
            dropdown.setCurrentIndex(self.options.index(value))

    def get_value(self) -> list[str]:
        return [dropdown.currentText() for dropdown in self.elements]
