from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QDialogButtonBox, QWidget
from PySide6.QtCore import Qt, QDateTime

class ProjectConfigDialog(QDialog):
    def __init__(self, parent, config):
        super(ProjectConfigDialog, self).__init__(parent)
        
        self._config = config
        layout = QVBoxLayout(self)
        self._addLineEditWithLabel(layout, 'Moodle username:', 'username')
        self._addLineEditWithLabel(layout, 'Moodle password:', 'password')
        self._addLineEditWithLabel(layout, 'Moodle server URL:', 'server_url')
        self._addLineEditWithLabel(layout, 'Moodle course shortname:', 'course_shortname')
        self._addLineEditWithLabel(layout, 'Moodle submissions directory:', 'moodle_submissions_dir')
        self._addLineEditWithLabel(layout, 'Assignment regex:', 'assignment_regex')
        self._addLineEditWithLabel(layout, 'Username conversions:', 'username_conversions')
        self._addLineEditWithLabel(layout, 'Assignment conversions:', 'assignment_conversions')
        self._addLineEditWithLabel(layout, 'JPlag arguments:', 'jplag_args')

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        layout.addWidget(buttons)
        self.setWindowTitle('Project Settings')

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        self._loadConfigValues()

    def _addLineEditWithLabel(self, layout, label, line_edit_name):
        new_layout = QHBoxLayout()
        new_layout.addWidget(QLabel(label))
        new_layout.addWidget(QLineEdit(self, objectName = line_edit_name))
        e = QWidget(self)
        e.setLayout(new_layout)
        layout.addWidget(e)

    def _loadConfigValues(self):
        # TODO: should be str in config perhaps; so need to fix it in the command line tools so they expect stringified lists
        widgets_values = [(self.findChild(QLineEdit, key), self._config[key]) for key in self._config]
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
