# FINAL PROJECT FLASHCARD APP / ui / pages / setttings_page.py


from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QCheckBox, QSlider, QComboBox,
    QGroupBox, QPushButton, QColorDialog, QMessageBox, QSpinBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon, QFont


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_color = "#FFFFFF"  
        self.notifications_enabled = False  
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setStyleSheet("color: black; background-color: white;")

        title = QLabel("<h1>Application Settings</h1>")

        #Notification settings
        notify_group = QGroupBox("Notifications")
        notify_layout = QVBoxLayout()

        #"Enable Notifications" checkbox
        self.enable_notify_check = QCheckBox("Enable notifications")
        self.enable_notify_check.stateChanged.connect(self.toggle_enable_notifications)

        #Existing "Play sound" checkbox
        self.sound_check = QCheckBox("Play sound")
        self.sound_check.setEnabled(False)  

        #Volume tracker (slider + label)
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setEnabled(False)

        self.volume_label = QLabel("Volume: 50%")

        #Enable/disable volume slider when "Play sound" is checked
        self.sound_check.stateChanged.connect(
            lambda state: self.volume_slider.setEnabled(
                state == Qt.CheckState.Checked.value and self.notifications_enabled
            )
        )

        #Update label when slider moves
        self.volume_slider.valueChanged.connect(
            lambda value: self.volume_label.setText(f"Volume: {value}%")
        )

        #Add widgets to notification layout
        notify_layout.addWidget(self.enable_notify_check)
        notify_layout.addWidget(self.sound_check)
        notify_layout.addWidget(self.volume_slider)
        notify_layout.addWidget(self.volume_label)
        notify_group.setLayout(notify_layout)

        #Appearance settings
        theme_group = QGroupBox("Appearance")
        theme_layout = QVBoxLayout()

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "Auto"])
        self.theme_combo.currentTextChanged.connect(self.apply_theme)

        theme_layout.addWidget(QLabel("Theme:"))
        theme_layout.addWidget(self.theme_combo)
        theme_group.setLayout(theme_layout)

        #Font settings
        font_group = QGroupBox("Font Settings")
        font_layout = QVBoxLayout()

        self.font_size = QSpinBox()
        self.font_size.setRange(8, 40)
        self.font_size.setValue(14)
        self.font_size.valueChanged.connect(self.apply_font_size)

        font_layout.addWidget(QLabel("Font Size:"))
        font_layout.addWidget(self.font_size)
        font_group.setLayout(font_layout)

        #Color settings
        color_group = QGroupBox("Background Color")
        color_layout = QVBoxLayout()

        self.color_button = QPushButton("Choose Color")
        self.color_button.clicked.connect(self.choose_color)

        color_layout.addWidget(self.color_button)
        color_group.setLayout(color_layout)

        #Save button
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)

        #Add all groups to layout
        layout.addWidget(title)
        layout.addWidget(notify_group)
        layout.addWidget(theme_group)
        layout.addWidget(font_group)
        layout.addWidget(color_group)
        layout.addWidget(self.save_button)
        layout.addStretch()

        self.setLayout(layout)


    def toggle_enable_notifications(self, state):
        """Enable or disable all notification options."""
        self.notifications_enabled = state == Qt.CheckState.Checked.value
        self.sound_check.setEnabled(self.notifications_enabled)
        self.volume_slider.setEnabled(False)
        if not self.notifications_enabled:
            self.sound_check.setChecked(False)

    def apply_theme(self, theme_name):
        """Apply dark/light theme across the app."""
        if theme_name == "Light":
            self.setStyleSheet("background-color: white; color: black;")
        elif theme_name == "Dark":
            self.setStyleSheet("background-color: #2b2b2b; color: white;")
        else:  
            self.setStyleSheet("background-color: white; color: black;")

    def apply_font_size(self, size):
        """Change font size for the entire interface."""
        font = QFont()
        font.setPointSize(size)
        self.setFont(font)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.selected_color = color.name()
            self.setStyleSheet(f"background-color: {self.selected_color}; color: black;")
            self.show_success_message(
                "Color Selected",
                f"Chosen color: {self.selected_color}"
            )

    def save_settings(self):
        theme = self.theme_combo.currentText()
        font_size = self.font_size.value()
        color = getattr(self, "selected_color", "#FFFFFF")
        volume = self.volume_slider.value()
        notifications = "Enabled" if self.notifications_enabled else "Disabled"

        self.show_success_message(
            "Success!",
            f"Settings saved successfully!\n\n"
            f"Notifications: {notifications}\n"
            f"Theme: {theme}\n"
            f"Font Size: {font_size}\n"
            f"Background: {color}\n"
            f"Volume: {volume}%"
        )

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





