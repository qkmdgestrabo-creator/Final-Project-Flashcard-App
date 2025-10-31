from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton

class HelpPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel("<h1>Help & Support</h1>")
        
        
        
        layout.addWidget(title)
        layout.addStretch()
        
        self.setLayout(layout)