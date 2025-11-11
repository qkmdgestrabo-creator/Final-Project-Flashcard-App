# FINAL PROJECT FLASHCARD APP / ui / pages / setttings_page.py


from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QCheckBox, QSlider, QComboBox,
    QGroupBox, QPushButton, QColorDialog, QMessageBox, QSpinBox, QApplication
)
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QPixmap, QIcon, QFont
import sys


class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_color = "#FFFFFF"
        self.notifications_enabled = False
        self.settings = QSettings("MyApp", "SettingsPage")  
        self.setup_ui()
        self.load_settings()  

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setStyleSheet("color: black; background-color: white;")

        title = QLabel("<h1>Application Settings</h1>")

        # Notification settings
        notify_group = QGroupBox("Notifications")
        notify_layout = QVBoxLayout()

        self.enable_notify_check = QCheckBox("Enable notifications")
        self.enable_notify_check.stateChanged.connect(self.toggle_enable_notifications)

        self.sound_check = QCheckBox("Play sound")
        self.sound_check.setEnabled(False)

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setEnabled(False)

        self.volume_label = QLabel("Volume: 50%")

        self.sound_check.stateChanged.connect(
            lambda state: self.volume_slider.setEnabled(
                state == Qt.CheckState.Checked.value and self.notifications_enabled
            )
        )
        self.volume_slider.valueChanged.connect(
            lambda value: self.volume_label.setText(f"Volume: {value}%")
        )

        notify_layout.addWidget(self.enable_notify_check)
        notify_layout.addWidget(self.sound_check)
        notify_layout.addWidget(self.volume_slider)
        notify_layout.addWidget(self.volume_label)
        notify_group.setLayout(notify_layout)

        # Appearance settings
        theme_group = QGroupBox("Appearance")
        theme_layout = QVBoxLayout()

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "Auto"])
        self.theme_combo.currentTextChanged.connect(self.apply_theme)

        theme_layout.addWidget(QLabel("Theme:"))
        theme_layout.addWidget(self.theme_combo)
        theme_group.setLayout(theme_layout)

        # Font settings 
        font_group = QGroupBox("Font Settings")
        font_layout = QVBoxLayout()

        self.font_size = QSpinBox()
        self.font_size.setRange(8, 40)
        self.font_size.setValue(14)
        self.font_size.valueChanged.connect(self.apply_font_size)

        font_layout.addWidget(QLabel("Font Size:"))
        font_layout.addWidget(self.font_size)
        font_group.setLayout(font_layout)

        # Background color
        color_group = QGroupBox("Background Color")
        color_layout = QVBoxLayout()

        self.color_button = QPushButton("Choose Color")
        self.color_button.clicked.connect(self.choose_color)

        color_layout.addWidget(self.color_button)
        color_group.setLayout(color_layout)

        # Save button
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)

        # Add all groups 
        layout.addWidget(title)
        layout.addWidget(notify_group)
        layout.addWidget(theme_group)
        layout.addWidget(font_group)
        layout.addWidget(color_group)
        layout.addWidget(self.save_button)
        layout.addStretch()
        self.setLayout(layout)

    # SETTINGS LOGIC 

    def toggle_enable_notifications(self, state):
        self.notifications_enabled = state == Qt.CheckState.Checked.value
        self.sound_check.setEnabled(self.notifications_enabled)
        self.volume_slider.setEnabled(False)
        if not self.notifications_enabled:
            self.sound_check.setChecked(False)

    def apply_theme(self, theme_name):
        """Apply theme across the entire app (not just this page)."""
        app = QApplication.instance()
        if theme_name == "Dark":
            app.setStyleSheet("QWidget { background-color: #2b2b2b; color: white; }")
        elif theme_name == "Light":
            app.setStyleSheet("QWidget { background-color: white; color: black; }")
        else:  
            app.setStyleSheet("QWidget { background-color: white; color: black; }")

    def apply_font_size(self, size):
        """Change font size for the entire app dynamically."""
        font = QFont()
        font.setPointSize(size)
        QApplication.instance().setFont(font)  

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.selected_color = color.name()
            app = QApplication.instance()
            app.setStyleSheet(f"QWidget {{ background-color: {self.selected_color}; color: black; }}")
            self.show_success_message("Color Selected", f"Chosen color: {self.selected_color}")

    def save_settings(self):
        """Save settings persistently using QSettings."""
        self.settings.setValue("theme", self.theme_combo.currentText())
        self.settings.setValue("font_size", self.font_size.value())
        self.settings.setValue("color", self.selected_color)
        self.settings.setValue("volume", self.volume_slider.value())
        self.settings.setValue("notifications", self.notifications_enabled)

        self.show_success_message(
            "Success!",
            f"Settings saved successfully!\n\n"
            f"Notifications: {'Enabled' if self.notifications_enabled else 'Disabled'}\n"
            f"Theme: {self.theme_combo.currentText()}\n"
            f"Font Size: {self.font_size.value()}\n"
            f"Background: {self.selected_color}\n"
            f"Volume: {self.volume_slider.value()}%"
        )

    def load_settings(self):
        """Load previously saved settings."""
        theme = self.settings.value("theme", "Light")
        font_size = int(self.settings.value("font_size", 14))
        color = self.settings.value("color", "#FFFFFF")
        volume = int(self.settings.value("volume", 50))
        notifications = self.settings.value("notifications", False, type=bool)

        # Apply saved values
        self.theme_combo.setCurrentText(theme)
        self.font_size.setValue(font_size)
        self.selected_color = color
        self.volume_slider.setValue(volume)
        self.enable_notify_check.setChecked(notifications)

        self.apply_theme(theme)
        self.apply_font_size(font_size)

    # UI HELPER 

    def show_success_message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.NoIcon)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)

        icon_path = "success.png"
        msg.setIconPixmap(QPixmap(icon_path).scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio))
        msg.setWindowIcon(QIcon(icon_path))

        msg.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
                color: #000000;
                font-size: 13px;
            }
            QLabel {
                color: #000000;
            }
            QPushButton {
                background-color: #cde5d4;
                color: black;
                border-radius: 8px;
                padding: 6px 25px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b4dbb8;
            }
        """)

        msg.exec()







