from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QCheckBox, 
    QSlider, QComboBox, QGroupBox
)

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel("<h1>Application Settings</h1>")
        
        # Notification settings group
        notify_group = QGroupBox("Notifications")
        notify_layout = QVBoxLayout()
        
        self.notify_check = QCheckBox("Enable notifications")
        self.sound_check = QCheckBox("Play sound")
        
        notify_layout.addWidget(self.notify_check)
        notify_layout.addWidget(self.sound_check)
        notify_group.setLayout(notify_layout)
        
        # Theme settings group
        theme_group = QGroupBox("Appearance")
        theme_layout = QVBoxLayout()
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "Auto"])
        
        theme_layout.addWidget(QLabel("Theme:"))
        theme_layout.addWidget(self.theme_combo)
        theme_group.setLayout(theme_layout)
        
        layout.addWidget(title)
        layout.addWidget(notify_group)
        layout.addWidget(theme_group)
        layout.addStretch()
        
        self.setLayout(layout)