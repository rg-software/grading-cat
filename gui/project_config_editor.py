from dataclasses import dataclass
from typing import Union
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QFormLayout,
    QGridLayout,
    QScrollArea,
    QVBoxLayout,
    QPushButton,
)
from PySide6.QtWidgets import QLineEdit, QDialogButtonBox, QWidget
from PySide6.QtCore import Qt
from dotmap import DotMap
from ast import literal_eval


class MultiOptionWidget(QWidget):

    """
    Structure:
    - MultiOptionWidget
        - QScrollArea
            - QWidget
                - QGridLayout
                    - QLineEdit
                    - QPushButton
    """

    BUTTON_ADD_TEXT = "+"
    BUTTON_ADD_TOOLTIP = "Add new line"
    BUTTON_REMOVE_TEXT = "-"
    BUTTON_REMOVE_TOOLTIP = "Remove line"
    BUTTON_MAX_WIDTH = 50

    ROW_FIXED_HEIGHT = 20

    def __init__(self, input_object_name: str, input_tooltip_text: str = "") -> QWidget:
        super().__init__()
        self.input_object_name = input_object_name
        self.input_tooltip_text = input_tooltip_text

        self.grid_layout = QGridLayout(verticalSpacing=10)
        self.grid_layout.setColumnMinimumWidth(0, 100)
        self.grid_layout.setColumnMinimumWidth(1, 25)
        self.add_row()

        scrollable_widget = QScrollArea(
            widget=QWidget(layout=self.grid_layout),
            widgetResizable=True,
            verticalScrollBarPolicy=Qt.ScrollBarAlwaysOn,
            horizontalScrollBarPolicy=Qt.ScrollBarAlwaysOff,
        )

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scrollable_widget)

        self.setLayout(main_layout)

    # adding and deleting rows: https://stackoverflow.com/a/21222826/5517838
    def add_row(self) -> QLineEdit:
        rows = self.grid_layout.rowCount()
        columns = self.grid_layout.columnCount()

        for column in range(columns):
            if layout := self.grid_layout.itemAtPosition(rows - 1, column):
                if isinstance(widget := layout.widget(), QPushButton):
                    widget.setText(self.BUTTON_REMOVE_TEXT)
                    widget.setToolTip(self.BUTTON_REMOVE_TOOLTIP)
                    widget.clicked.disconnect(self.add_row)
                    # to specify which button is clicked
                    # ref: https://stackoverflow.com/a/20334117/5517838
                    widget.clicked.connect(lambda: self.delete_row(widget))

        line = QLineEdit(
            objectName=self.input_object_name,
            toolTip=self.input_tooltip_text,
            fixedHeight=self.ROW_FIXED_HEIGHT,
        )
        self.grid_layout.addWidget(line, rows, 0)

        button = QPushButton(
            text=self.BUTTON_ADD_TEXT,
            toolTip=self.BUTTON_ADD_TOOLTIP,
            fixedHeight=self.ROW_FIXED_HEIGHT,
            maximumWidth=self.BUTTON_MAX_WIDTH,
        )
        button.clicked.connect(self.add_row)
        self.grid_layout.addWidget(button, rows, columns - 1)

        return line

    def delete_row(self, button_clicked: QPushButton) -> None:
        index = self.grid_layout.indexOf(button_clicked)
        row = self.grid_layout.getItemPosition(index)[0]
        for column in range(self.grid_layout.columnCount()):
            if layout := self.grid_layout.itemAtPosition(row, column):
                layout.widget().deleteLater()
                self.grid_layout.removeItem(layout)


class ProjectConfigDialog(QDialog):
    @dataclass
    class ConfigSetting:
        display: str
        input: str
        tooltip: str = ""
        has_multi_value: bool = False

    config_settings = {
        "username": ConfigSetting(display="Moodle username:", input="username"),
        "password": ConfigSetting(display="Moodle password:", input="password"),
        "server_url": ConfigSetting(display="Moodle server URL:", input="server_url"),
        "course_shortname": ConfigSetting(
            display="Moodle course shortname:", input="course_shortname"
        ),
        "moodle_submissions_dir": ConfigSetting(
            display="Moodle submissions directory:",
            input="moodle_submissions_dir",
        ),
        "assignment_regex": ConfigSetting(
            display="Assignment regex:", input="assignment_regex"
        ),
        "username_conversions": ConfigSetting(
            display="Username conversions:",
            input="username_conversions",
            tooltip="Format: [['from-pattern-1', 'to-pattern-1'], ...]",
        ),
        "assignment_conversions": ConfigSetting(
            display="Assignment conversions:",
            input="assignment_conversions",
            tooltip="Format: [['from-pattern-1', 'to-pattern-1'], ...]",
        ),
        "archive_dirs": ConfigSetting(
            display="Archive directories: ", input="archive_dirs", has_multi_value=True
        ),
        "template_dir": ConfigSetting(
            display="Template directory: ", input="template_dir"
        ),
        "java_path": ConfigSetting(display="Java path:", input="java_path"),
        "jplag_args": ConfigSetting(
            display="JPlag arguments:",
            input="jplag_args",
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
            if setting.has_multi_value:
                self.add_multi_input_row(setting)
            else:
                self.add_single_input_row(setting)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self
        )
        self.form_layout.addRow(buttons)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        self.setLayout(self.form_layout)
        self._loadConfigValues()

    def add_single_input_row(self, setting: ConfigSetting) -> None:
        line_edit = QLineEdit(
            self,
            objectName=setting.input,
            toolTip=setting.tooltip,
        )
        self.form_layout.addRow(QLabel(setting.display), line_edit)

    def add_multi_input_row(self, setting: ConfigSetting):
        self.form_layout.addRow(
            QLabel(setting.display),
            MultiOptionWidget(
                setting.input,
                setting.tooltip,
            ),
        )

    def _loadConfigValues(self) -> None:
        widgets_values: list[tuple[QLineEdit, Union[str, list[str]]]] = [
            (self.findChildren(QLineEdit, key), self._config[key])
            for key in self._config
        ]
        for line_edits, values in [(w, v) for (w, v) in widgets_values if w]:
            if len(line_edits) == 1 and isinstance(values, str):
                if line_edits[0].objectName() == "jplag_args":
                    jplag_args_list = literal_eval(values)
                    try:
                        bc_index = jplag_args_list.index("-bc")
                    except ValueError:
                        print("No template directory defined.")
                    else:
                        jplag_args_list.pop(bc_index)  # remove "-bc"
                        jplag_args_list.pop(bc_index)  # remove template_dir
                        values = repr(jplag_args_list) if jplag_args_list else ""
                line_edits[0].setText(values)
                continue

            # make number of QLineEdit matches number of values
            while len(line_edits) < len(values):
                assert isinstance(
                    multi_option_widget := line_edits[0]
                    .parent()
                    .parent()
                    .parent()
                    .parent(),
                    MultiOptionWidget,
                )
                # ? is there a better way than calling parent() many times?
                line_edits.append(multi_option_widget.add_row())

            for line_edit, value in zip(line_edits, values):
                line_edit.setText(value)

    def _saveConfigValues(self) -> None:
        new_config = {}
        for line_edit in self.findChildren(QLineEdit):
            if not self.config_settings[line_edit.objectName()].has_multi_value:
                new_config[line_edit.objectName()] = line_edit.text()
                continue

            if line_edit.objectName() in new_config:
                new_config[line_edit.objectName()].append(line_edit.text())
            else:
                new_config[line_edit.objectName()] = [line_edit.text()]

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
