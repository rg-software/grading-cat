from abc import abstractmethod
from ast import literal_eval
from dataclasses import dataclass, field
from typing import Union

from dotmap import DotMap
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

# Note on regexp -> JSON: Add double backslashes to escape backslashes in regexp
USERNAME_CONVERSION_PRESETS = {"Keep email username only": "['(.+)@.+', '\\\\1']"}

ASSIGNMENT_CONVERSION_PRESETS = {
    "Extract assignment number (two digits)": "['.+(\\\\d\\\\d).+', '\\\\1']",
    "Extract assignment number (one digit)": "['.+(\\\\d).+', '0\\\\1']",
}


@dataclass
class ConfigSetting:
    display_name: str
    object_name: str
    tooltip: str = ""
    has_multi_value: bool = False
    options: dict[str, str] = field(
        default_factory=dict
    )  # {"regexp preset label": "regexp preset values"}


class UserInputWidget(QWidget):
    """Abstraction for user input fields."""

    def __init__(self, object_name: str):
        super().__init__(objectName=object_name)

    @abstractmethod
    def display_config(self, config_values: Union[str, list[str]]) -> None:
        ...

    @abstractmethod
    def get_config(self) -> Union[str, list[str]]:
        ...


class SingleLineInputWidget(UserInputWidget):
    def __init__(self, object_name: str, tooltip: str) -> None:
        super().__init__(object_name=object_name)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        # self._line_edit = QLineEdit(self, objectName=object_name, toolTip=tooltip)
        self._line_edit = QLineEdit(self, toolTip=tooltip)
        layout.addWidget(self._line_edit)

        self.setLayout(layout)

    def display_config(self, config_values: str) -> None:
        self._line_edit.setText(config_values)

    def get_config(self) -> Union[str, list[str]]:
        return self._line_edit.text()


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

    ROW_FIXED_HEIGHT = 20

    def __init__(self, object_name: str) -> None:
        super().__init__(object_name=object_name)

        add_button = QPushButton(
            text=self.BUTTON_ADD_TEXT,
            toolTip=self.BUTTON_ADD_TOOLTIP,
            fixedHeight=self.ROW_FIXED_HEIGHT + 10,
            maximumWidth=self.BUTTON_MAX_WIDTH + 15,
        )
        add_button.clicked.connect(self.add_row)
        # not sure if this is the best way to align the button to right
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(add_button)

        self.grid_layout = QGridLayout(verticalSpacing=10)
        self.grid_layout.setColumnMinimumWidth(0, 100)
        self.grid_layout.setColumnMinimumWidth(1, 25)
        self.add_row()

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

    def add_row(self) -> None:
        rows = self.grid_layout.rowCount()
        columns = self.grid_layout.columnCount()

        line = self.create_input()
        self.grid_layout.addWidget(line, rows, 0)

        button = QPushButton(
            text=self.BUTTON_REMOVE_TEXT,
            toolTip=self.BUTTON_REMOVE_TEXT,
            fixedHeight=self.ROW_FIXED_HEIGHT,
            maximumWidth=self.BUTTON_MAX_WIDTH,
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
                layout.widget().deleteLater()
                self.grid_layout.removeItem(layout)


class MultilineInputWidget(MultilineWidget):
    def __init__(self, object_name: str, tooltip: str) -> None:
        self.tooltip = tooltip
        self.lines: list[QLineEdit] = []
        super().__init__(object_name=object_name)

    def create_input(self) -> QLineEdit:
        self.lines.append(
            QLineEdit(
                toolTip=self.tooltip,
                fixedHeight=self.ROW_FIXED_HEIGHT,
            )
        )
        return self.lines[-1]

    def display_config(self, config_values: list[str]) -> None:
        while len(self.lines) < len(config_values):
            self.add_row()

        for line, value in zip(self.lines, config_values):
            line.setText(value)

    def get_config(self) -> list[str]:
        return list({line.text() for line in self.lines})  # prevent duplicates


class MultiDropdownWidget(MultilineWidget):
    def __init__(self, object_name: str, tooltip: str, options: dict) -> None:
        self.tooltip = tooltip
        self.options = options
        self.dropdowns: list[QComboBox] = []
        super().__init__(object_name=object_name)

    def create_input(self) -> QComboBox:
        self.dropdowns.append(
            QComboBox(
                toolTip=self.tooltip,
            )
        )
        self.dropdowns[-1].addItems(self.options.keys())
        return self.dropdowns[-1]

    def display_config(self, config_values: list[str]) -> None:
        while len(self.dropdowns) < len(config_values):
            self.add_row()

        for dropdown, value in zip(self.dropdowns, config_values):
            dropdown.setCurrentIndex(list(self.options.values()).index(value))

    def get_config(self) -> list[str]:
        return [
            self.options[key]
            for key in {dropdown.currentText() for dropdown in self.dropdowns}
        ]


class ProjectConfigDialog(QDialog):

    config_settings = {
        "username": ConfigSetting(
            display_name="Moodle username:", object_name="username"
        ),
        "password": ConfigSetting(
            display_name="Moodle password:", object_name="password"
        ),
        "server_url": ConfigSetting(
            display_name="Moodle server URL:", object_name="server_url"
        ),
        "course_shortname": ConfigSetting(
            display_name="Moodle course shortname:", object_name="course_shortname"
        ),
        "moodle_submissions_dir": ConfigSetting(
            display_name="Moodle submissions directory:",
            object_name="moodle_submissions_dir",
        ),
        "assignment_regex": ConfigSetting(
            display_name="Assignment regex:", object_name="assignment_regex"
        ),
        "username_conversions": ConfigSetting(
            display_name="Username conversions:",
            object_name="username_conversions",
            tooltip="Format: [['from-pattern-1', 'to-pattern-1'], ...]",
            has_multi_value=True,
            options=USERNAME_CONVERSION_PRESETS,
        ),
        "assignment_conversions": ConfigSetting(
            display_name="Assignment conversions:",
            object_name="assignment_conversions",
            tooltip="Format: [['from-pattern-1', 'to-pattern-1'], ...]",
            has_multi_value=True,
            options=ASSIGNMENT_CONVERSION_PRESETS,
        ),
        "archive_dirs": ConfigSetting(
            display_name="Archive directories: ",
            object_name="archive_dirs",
            has_multi_value=True,
        ),
        "template_dir": ConfigSetting(
            display_name="Template directory: ", object_name="template_dir"
        ),
        "java_path": ConfigSetting(display_name="Java path:", object_name="java_path"),
        "jplag_args": ConfigSetting(
            display_name="JPlag arguments:",
            object_name="jplag_args",
            tooltip="Format: ['arg-1', 'arg-2', ...]",
        ),
    }

    def __init__(self, parent: QWidget, config: DotMap) -> None:
        super().__init__(parent)

        # TODO: better editing options for:
        # - regular expressions
        # - presets

        self._config = config
        self.setWindowTitle("Project Settings")

        self.form_layout = QFormLayout(verticalSpacing=15)

        for setting in self.config_settings.values():
            if setting.options:
                self.form_layout.addRow(
                    QLabel(setting.display_name),
                    MultiDropdownWidget(
                        object_name=setting.object_name,
                        tooltip=setting.tooltip,
                        options=setting.options,
                    ),
                )
            elif setting.has_multi_value:
                self.form_layout.addRow(
                    QLabel(setting.display_name),
                    MultilineInputWidget(
                        object_name=setting.object_name, tooltip=setting.tooltip
                    ),
                )
            else:
                self.form_layout.addRow(
                    QLabel(setting.display_name),
                    SingleLineInputWidget(
                        object_name=setting.object_name, tooltip=setting.tooltip
                    ),
                )

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self
        )
        self.form_layout.addRow(buttons)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        self.setLayout(self.form_layout)
        self._loadConfigValues()

    def _loadConfigValues(self) -> None:
        widgets_values = [
            (self.findChild(UserInputWidget, key), value)
            for (key, value) in self._config.items()
        ]

        user_input: UserInputWidget
        for user_input, values in [(w, v) for (w, v) in widgets_values if w]:
            if user_input.objectName() == "jplag_args":
                jplag_args_list = literal_eval(values)
                try:
                    bc_index = jplag_args_list.index("-bc")
                except ValueError:
                    print("No template directory defined.")
                else:
                    jplag_args_list.pop(bc_index)  # remove "-bc"
                    jplag_args_list.pop(bc_index)  # remove template_dir
                    values = repr(jplag_args_list)

            user_input.display_config(values)

    def _saveConfigValues(self) -> None:
        new_config = {}

        user_input: UserInputWidget
        for user_input in self.findChildren(UserInputWidget):
            new_config[user_input.objectName()] = user_input.get_config()

        # post-process to map template_dir back into jplag_args
        if new_config["template_dir"]:
            if new_config["jplag_args"]:
                try:
                    jplag_args_list = literal_eval(new_config["jplag_args"])
                    jplag_args_list.extend(["-bc", new_config["template_dir"]])
                except (ValueError, SyntaxError, AttributeError):
                    # ValueError and SyntaxError: sending malformed string into literal_eval
                    # AttributeError: trying to use extend on a non-list object
                    # ? is replacing the values the best solution here?
                    jplag_args_list = ["-bc", new_config["template_dir"]]
            else:
                jplag_args_list = ["-bc", new_config["template_dir"]]

            new_config["jplag_args"] = repr(jplag_args_list)

        self._config = DotMap(new_config)

    @staticmethod
    def show(parent, config) -> tuple[bool, DotMap]:
        dialog = ProjectConfigDialog(parent, config)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            dialog._saveConfigValues()
        return result == QDialog.Accepted, dialog._config
