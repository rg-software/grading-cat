from dataclasses import dataclass, field

from dotmap import DotMap
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QWidget, QFormLayout, QLabel, QDialogButtonBox

from gui.config_editor_widgets import MultiDropdownWidget, SingleDropdownWidget
from gui.config_editor_widgets import MultilineInputWidget, SingleLineInputWidget


@dataclass
class ConfigSetting:
    display_name: str
    object_name: str
    tooltip: str = ""
    has_multi_value: bool = False
    options: list[str] = field(default_factory=list)
    widget: object = None


class ProjectConfigDialog(QDialog):
    config_settings = [
        ConfigSetting(display_name="Moodle username:", object_name="username"),
        ConfigSetting(display_name="Moodle password:", object_name="password"),
        ConfigSetting(display_name="Moodle server URL:", object_name="server_url"),
        ConfigSetting(display_name="Moodle service:", object_name="moodle_service"),
        ConfigSetting(
            display_name="Moodle course shortname:", object_name="course_shortname"
        ),
        ConfigSetting(
            display_name="Assignment regexes:",
            object_name="assignment_regexes",
            tooltip="Info :: pattern",
            has_multi_value=True,
            options="assignment_regexes_presets",
        ),
        ConfigSetting(
            display_name="Username conversions:",
            object_name="username_conversions",
            tooltip="Info :: from-pattern :: to-pattern",
            has_multi_value=True,
            options="username_conversions_presets",
        ),
        ConfigSetting(
            display_name="Assignment conversions:",
            object_name="assignment_conversions",
            tooltip="Info :: from-pattern :: to-pattern",
            has_multi_value=True,
            options="assignment_conversions_presets",
        ),
        ConfigSetting(
            display_name="Archive directories:",
            object_name="archive_dirs",
            has_multi_value=True,
        ),
        ConfigSetting(display_name="Template directory:", object_name="template_dir"),
        ConfigSetting(
            display_name="Language parser:",
            object_name="language",
            has_multi_value=False,
            options="language_presets",
        ),
        ConfigSetting(display_name="Java path:", object_name="java_path"),
    ]

    def _makeWidget(self, setting):
        multivalue = setting.has_multi_value
        options = setting.options
        obj = setting.object_name
        hint = setting.tooltip
        opts = [] if not setting.options else self._config[setting.options]

        if multivalue and options:  # a group of combo boxes
            return MultiDropdownWidget(object_name=obj, tooltip=hint, options=opts)
        elif not multivalue and options:  # a single combo box
            return SingleDropdownWidget(object_name=obj, tooltip=hint, options=opts)
        elif multivalue:  # a group of single-line inputs
            return MultilineInputWidget(object_name=obj, tooltip=hint)
        else:  # a single-line input box
            return SingleLineInputWidget(object_name=obj, tooltip=hint)

    def __init__(self, parent: QWidget, config: DotMap) -> None:
        super().__init__(parent)

        self._config = config
        self.setWindowTitle("Project Settings")
        self.form_layout = QFormLayout(verticalSpacing=15)

        for setting in self.config_settings:
            label = QLabel(setting.display_name)
            setting.widget = self._makeWidget(setting)
            self.form_layout.addRow(label, setting.widget)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self
        )
        self.form_layout.addRow(buttons)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        self.setLayout(self.form_layout)
        self._loadConfigValues()

    def _loadConfigValues(self) -> None:
        for widget, value in [(s.widget, s.object_name) for s in self.config_settings]:
            widget.display_value(self._config[value])

    def _saveConfigValues(self) -> None:
        for widget in [s.widget for s in self.config_settings]:
            self._config[widget.objectName()] = widget.get_value()

    @staticmethod
    def show(parent, config) -> tuple[bool, DotMap]:
        dialog = ProjectConfigDialog(parent, config)
        result = dialog.exec()
        if result == QDialog.Accepted:
            dialog._saveConfigValues()
        return result == QDialog.Accepted, dialog._config
