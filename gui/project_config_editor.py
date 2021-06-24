from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QLineEdit, QDialogButtonBox, QWidget
from PySide6.QtCore import Qt


class ProjectConfigDialog(QDialog):
    def __init__(self, parent, config):
        super().__init__(parent)

        # TODO: better editing options for:
        # - regular expressions
        # - presets
        self._config = config
        lt = QVBoxLayout(self)
        self._addLineEdit(lt, "Moodle username:", "username")
        self._addLineEdit(lt, "Moodle password:", "password")
        self._addLineEdit(lt, "Moodle server URL:", "server_url")
        self._addLineEdit(lt, "Moodle course shortname:", "course_shortname")
        self._addLineEdit(lt, "Moodle submissions directory:", "moodle_submissions_dir")
        self._addLineEdit(lt, "Assignment regex:", "assignment_regex")
        self._addLineEdit(lt, "Username conversions:", "username_conversions")
        self._addLineEdit(lt, "Assignment conversions:", "assignment_conversions")
        self._addLineEdit(lt, "Java path:", "java_path")
        self._addLineEdit(lt, "JPlag arguments:", "jplag_args")

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self
        )
        lt.addWidget(buttons)
        self.setWindowTitle("Project Settings")

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        self._loadConfigValues()

    def _addLineEdit(self, layout, label, line_edit_name):
        new_layout = QHBoxLayout()
        new_layout.addWidget(QLabel(label))
        new_layout.addWidget(QLineEdit(self, objectName=line_edit_name))
        e = QWidget(self)
        e.setLayout(new_layout)
        layout.addWidget(e)

    def _loadConfigValues(self):
        widgets_values = [
            (self.findChild(QLineEdit, key), self._config[key]) for key in self._config
        ]
        for line_edit, value in [(w, v) for (w, v) in widgets_values if w]:
            line_edit.setText(value)

    def _saveConfigValues(self):
        for line_edit in self.findChildren(QLineEdit):
            self._config[line_edit.objectName()] = line_edit.text()

    @staticmethod
    def show(parent, config):
        dialog = ProjectConfigDialog(parent, config)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            dialog._saveConfigValues()
        return result == QDialog.Accepted, dialog._config
