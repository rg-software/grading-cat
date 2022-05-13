from PySide6.QtWidgets import QDialog, QLabel, QFormLayout
from PySide6.QtWidgets import QLineEdit, QDialogButtonBox, QWidget
from PySide6.QtCore import Qt
from dotmap import DotMap


class ProjectConfigDialog(QDialog):
    def __init__(self, parent: QWidget, config: DotMap) -> None:
        super().__init__(parent)

        # TODO: better editing options for:
        # - regular expressions
        # - presets
        self._config = config
        self.setWindowTitle("Project Settings")

        self.form_layout = QFormLayout(verticalSpacing=15)

        self.add_single_input_row("Moodle username:", "username")
        self.add_single_input_row("Moodle password:", "password")
        self.add_single_input_row("Moodle server URL:", "server_url")
        self.add_single_input_row("Moodle course shortname:", "course_shortname")
        self.add_single_input_row(
            "Moodle submissions directory:", "moodle_submissions_dir"
        )
        self.add_single_input_row("Assignment regex:", "assignment_regex")
        self.add_single_input_row("Username conversions:", "username_conversions")
        self.add_single_input_row("Assignment conversions:", "assignment_conversions")
        self.add_single_input_row("Java path:", "java_path")
        self.add_single_input_row("JPlag arguments:", "jplag_args")

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self
        )
        self.form_layout.addRow(buttons)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        self.setLayout(self.form_layout)
        self._loadConfigValues()

    def add_single_input_row(
        self, label: str, line_edit_name: str, placeholder_text: str = ""
    ) -> None:
        line_edit = QLineEdit(
            self, objectName=line_edit_name, placeholderText=placeholder_text
        )
        self.form_layout.addRow(QLabel(label), line_edit)

    def _loadConfigValues(self) -> None:
        widgets_values = [
            (self.findChild(QLineEdit, key), self._config[key]) for key in self._config
        ]
        for line_edit, value in [(w, v) for (w, v) in widgets_values if w]:
            line_edit.setText(value)

    def _saveConfigValues(self) -> None:
        for line_edit in self.findChildren(QLineEdit):
            self._config[line_edit.objectName()] = line_edit.text()

    @staticmethod
    def show(parent, config) -> tuple[bool, DotMap]:
        dialog = ProjectConfigDialog(parent, config)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            dialog._saveConfigValues()
        return result == QDialog.Accepted, dialog._config
